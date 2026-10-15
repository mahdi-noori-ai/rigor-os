#!/usr/bin/env python3
"""Rigor OS shell guard — one deterministic pre-execution hook for every adapter.

Reads a hook payload on stdin and blocks destructive or secret-leaking shell
commands. Speaks three dialects, detected from the payload:

* Claude Code ``PreToolUse``  -> ``hookSpecificOutput.permissionDecision``
* OpenAI Codex ``PreToolUse`` -> same shape as Claude Code
* Cursor ``beforeShellExecution`` -> ``{"permission": "allow" | "deny"}``

Stdlib only, so it runs anywhere ``python3`` exists. Unknown payloads are
allowed (fail-open) except under Cursor, where ``failClosed`` decides.
"""

from __future__ import annotations

import json
import re
import shlex
import sys
from dataclasses import dataclass

SEPARATORS = re.compile(r"\|\||&&|[;|&\n]|\$\(|`")

DANGEROUS_RM_TARGETS = {
    "/",
    "/*",
    "~",
    "~/",
    "~/*",
    "$HOME",
    "${HOME}",
    "$HOME/",
    "${HOME}/",
    "$HOME/*",
    ".",
    "./",
    "..",
    "../",
    "*",
    "./*",
    "/bin",
    "/boot",
    "/dev",
    "/etc",
    "/home",
    "/lib",
    "/opt",
    "/root",
    "/sbin",
    "/srv",
    "/usr",
    "/var",
    "/Users",
    "/System",
    "/Library",
    "/Applications",
}

PROTECTED_BRANCHES = re.compile(r"(^|[:+/\s])(main|master|trunk|production|prod|release[\w./-]*)$")


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    reason: str


RULES: tuple[Rule, ...] = (
    Rule(
        "sql-destructive-ddl",
        re.compile(r"\bDROP\s+(DATABASE|SCHEMA|TABLE|ROLE|USER|OWNED)\b", re.I),
        "Destructive SQL DDL (DROP ...). Needs explicit user approval and a rollback plan.",
    ),
    Rule(
        "sql-truncate",
        re.compile(r"\bTRUNCATE\s+(TABLE\s+)?(ONLY\s+)?\"?[A-Za-z_][\w.\"]*\"?\s*(,|;|CASCADE|RESTART|$)", re.I),
        "TRUNCATE wipes table data. Needs explicit user approval.",
    ),
    Rule(
        "disk-format",
        re.compile(r"\b(mkfs(\.\w+)?|wipefs|diskutil\s+(erase\w*|zeroDisk|secureErase))\b"),
        "Formatting or wiping a disk is irreversible.",
    ),
    Rule(
        "raw-device-write",
        re.compile(r"\bdd\b[^|;&]*\bof=/dev/|>\s*/dev/(sd|nvme|disk|hd)\w*"),
        "Raw writes to a block device are irreversible.",
    ),
    Rule(
        "fork-bomb",
        re.compile(r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:"),
        "Fork bomb.",
    ),
    Rule(
        "chmod-world-root",
        re.compile(r"\bchmod\s+(-\w*R\w*\s+)?(0?777|a\+rwx)\s+/(\s|$)"),
        "Recursive world-writable permissions on the filesystem root.",
    ),
    Rule(
        "pipe-to-shell",
        re.compile(r"\b(curl|wget|iwr|Invoke-WebRequest)\b[^|]*\|\s*(sudo\s+)?(ba|z|da|k)?sh\b"),
        "Piping a remote script into a shell is an unreviewed supply-chain install. "
        "Download, inspect, and justify it first.",
    ),
    Rule(
        "print-secrets",
        re.compile(
            r"\b(cat|less|more|head|tail|bat|type|strings|xxd|base64)\b[^|;&]*"
            r"(^|[\s/'\"])\.env(\.(?!example\b|sample\b|template\b)[\w.-]+)?(?=$|[\s'\"])"
        ),
        "Printing .env exposes secrets into the transcript. Read .env.example instead.",
    ),
    Rule(
        "docker-volume-wipe",
        re.compile(
            r"\bdocker\b[^;&|]*\b(compose\b[^;&|]*\bdown\b[^;&|]*(\s-v\b|--volumes\b)"
            r"|volume\s+(rm|prune)\b|system\s+prune\b[^;&|]*--volumes\b)"
        ),
        "This deletes Docker volumes (database data). Ask the user first.",
    ),
    Rule(
        "infra-destroy",
        re.compile(
            r"\b(terraform|tofu)\s+(destroy|apply\b[^;&|]*-destroy)\b"
            r"|\bkubectl\s+delete\s+(ns|namespace|pv|pvc|all)\b"
            r"|\bhelm\s+uninstall\b"
        ),
        "Infrastructure teardown. Needs explicit user approval.",
    ),
)


def segments(command: str) -> list[str]:
    return [s.strip() for s in SEPARATORS.split(command) if s.strip()]


def tokens(segment: str) -> list[str]:
    try:
        parts = shlex.split(segment, posix=True)
    except ValueError:
        parts = segment.split()
    return [p.strip("'\"") for p in parts]


def _strip_wrappers(words: list[str]) -> list[str]:
    wrappers = {"sudo", "doas", "command", "builtin", "nohup", "time", "nice", "env", "xargs"}
    i = 0
    while i < len(words) and (words[i] in wrappers or re.match(r"^[A-Za-z_]\w*=", words[i])):
        i += 1
    return words[i:]


def check_rm(words: list[str]) -> str | None:
    words = _strip_wrappers(words)
    if not words or words[0].rsplit("/", 1)[-1] != "rm":
        return None
    flags = set()
    targets = []
    for w in words[1:]:
        if w == "--no-preserve-root":
            return "rm --no-preserve-root is never acceptable."
        if w in ("--recursive", "-R"):
            flags.add("r")
        elif w == "--force":
            flags.add("f")
        elif w.startswith("-") and not w.startswith("--"):
            flags.update(w[1:].lower())
        else:
            targets.append(w)
    if "r" not in flags:
        return None
    for t in targets:
        if t in DANGEROUS_RM_TARGETS or t.rstrip("/") in DANGEROUS_RM_TARGETS:
            return f"Recursive delete of '{t}' is irreversible. Ask the user first."
    return None


def check_git_push(words: list[str]) -> str | None:
    words = _strip_wrappers(words)
    if len(words) < 2 or words[0].rsplit("/", 1)[-1] != "git":
        return None
    # skip global options such as -C dir / -c k=v
    i = 1
    while i < len(words) and words[i].startswith("-"):
        i += 2 if words[i] in ("-C", "-c") else 1
    if i >= len(words) or words[i] != "push":
        return None
    args = words[i + 1 :]
    hard_force = any(a in ("--force", "-f") or (re.fullmatch(r"-[a-z]*f[a-z]*", a) is not None) for a in args)
    lease = any(a.startswith(("--force-with-lease", "--force-if-includes")) for a in args)
    refs = [a for a in args if not a.startswith("-")]
    plus_ref = any(r.startswith("+") for r in refs[1:])
    protected = any(PROTECTED_BRANCHES.search(r) for r in refs[1:]) or len(refs) <= 1
    if hard_force or plus_ref:
        return "Force push rewrites shared history. Ask the user first (prefer --force-with-lease on a feature branch)."
    if lease and protected:
        return "Force push to a protected or implicit branch. Name a feature branch explicitly."
    return None


def evaluate(command: str) -> str | None:
    """Return a block reason, or None when the command is allowed."""
    if not command or not command.strip():
        return None
    for seg in segments(command):
        words = tokens(seg)
        inner = _strip_wrappers(words)
        if inner and inner[0].rsplit("/", 1)[-1] in {"sh", "bash", "zsh", "dash", "ksh", "eval"}:
            script = inner[inner.index("-c") + 1] if "-c" in inner[:-1] else " ".join(inner[1:])
            if script != command:
                reason = evaluate(script)
                if reason:
                    return reason
        for check in (check_rm, check_git_push):
            reason = check(words)
            if reason:
                return reason
    for rule in RULES:
        if rule.pattern.search(command):
            return rule.reason
    return None


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}

    cursor = payload.get("hook_event_name") == "beforeShellExecution" or (
        "command" in payload and "tool_input" not in payload
    )
    if cursor:
        command = str(payload.get("command") or "")
    else:
        tool_input = payload.get("tool_input") or {}
        command = str(tool_input.get("command") or "") if isinstance(tool_input, dict) else ""

    reason = evaluate(command)
    prefix = "Rigor OS guard: "

    if cursor:
        if reason:
            msg = prefix + reason
            print(json.dumps({"permission": "deny", "user_message": msg, "agent_message": msg}))
        else:
            print(json.dumps({"permission": "allow"}))
        return 0

    if reason:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": prefix + reason,
                    }
                }
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
