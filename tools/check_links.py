#!/usr/bin/env python3
"""Fail when a Markdown file links to a repository path that does not exist.

Checks relative ``[text](path)`` links and backticked ``rigor-os/...`` references,
so renames cannot silently orphan skills, workflows, or gates.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
OS_REF = re.compile(r"`rigor-os/([\w./-]+?)`")
GENERATED = {"SEO_CONTEXT.md", "SEO_CONTEXT.json"}


def broken_links(md: Path) -> list[str]:
    text = md.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    problems = []
    for target in LINK.findall(text):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        path = target.split("#", 1)[0]
        if path and not (md.parent / path).exists():
            problems.append(f"{md.relative_to(ROOT)}: missing link target {target}")
    for ref in OS_REF.findall(text):
        ref = ref.rstrip("/.")
        if any(ch in ref for ch in "*{<") or Path(ref).name in GENERATED:
            continue
        if not (ROOT / ref).exists():
            problems.append(f"{md.relative_to(ROOT)}: missing rigor-os path {ref}")
    return problems


def main() -> int:
    problems = []
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts or "node_modules" in md.parts:
            continue
        problems += broken_links(md)
    print("\n".join(problems) or "links ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
