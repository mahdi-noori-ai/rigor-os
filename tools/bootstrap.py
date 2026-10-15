#!/usr/bin/env python3
"""Scan a repository and fill rigor-os/project-context templates.

Safe to re-run: files you have edited are kept unless you pass ``--force``.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "dist",
    "build",
    "out",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".astro",
    ".output",
    "coverage",
    "target",
    ".gradle",
    "Pods",
    "vendor",
    ".turbo",
    ".cache",
    "rigor-os",
    ".idea",
    "Library",
    "Temp",
    "obj",
}
TEMPLATE_MARKERS = ("<!-- rigor-os:template", "(fill via bootstrap)")
MAX_FILES = 20000


def find_root(start: Path) -> Path:
    p = start.resolve()
    for cand in [p, *p.parents]:
        if (cand / "rigor-os").is_dir():
            return cand
    return p


def scan(root: Path) -> list[Path]:
    """Walk the repo once, pruning dependency/build folders."""
    files: list[Path] = []
    stack = [root]
    while stack and len(files) < MAX_FILES:
        cur = stack.pop()
        try:
            entries = list(cur.iterdir())
        except OSError:
            continue
        for e in entries:
            if e.is_dir():
                if e.name not in SKIP_DIRS and not (
                    e.name.startswith(".") and e.name not in (".github", ".cursor", ".claude", ".codex", ".vscode")
                ):
                    stack.append(e)
            else:
                files.append(e)
    return files


def text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def mcp_servers(body: str, toml: bool) -> list[str]:
    if toml:
        return re.findall(r"^\s*\[mcp_servers\.([\w.-]+)\]", body, re.M)
    try:
        data = json.loads(body or "{}")
    except json.JSONDecodeError:
        return []
    return list((data.get("mcpServers") or data.get("servers") or {}).keys())


def detect(root: Path) -> dict:
    info: dict = {
        "backend": [],
        "frontend": [],
        "mobile": [],
        "database": [],
        "docker": False,
        "ci": [],
        "mcp": [],
        "seo_surface": False,
        "commands": {},
        "profile": "Medium",
    }
    files = scan(root)
    names = {f.name for f in files}
    rel = {str(f.relative_to(root)) for f in files}

    def add(key: str, value: str) -> None:
        if value not in info[key]:
            info[key].append(value)

    # ---- Python
    pyproject = text(root / "pyproject.toml")
    reqs = text(root / "requirements.txt")
    py_blob = (pyproject + reqs).lower()
    uv = (root / "uv.lock").exists()
    poetry = (root / "poetry.lock").exists()
    run = "uv run " if uv else "poetry run " if poetry else ""
    if (root / "manage.py").exists() or "django" in py_blob:
        add("backend", "Django")
        if "djangorestframework" in py_blob:
            add("backend", "DRF")
        info["commands"]["migrate"] = f"{run}python manage.py migrate"
    if "fastapi" in py_blob:
        add("backend", "FastAPI")
    if "flask" in py_blob:
        add("backend", "Flask")
    if pyproject or reqs:
        if not info["backend"]:
            add("backend", "Python")
        info["commands"]["test"] = f"{run}pytest"
        info["commands"]["lint"] = f"{run}ruff check ."
        info["commands"]["format"] = f"{run}ruff format --check ."
        if uv:
            info["commands"]["install"] = "uv sync --frozen"
        if "mypy" in py_blob:
            info["commands"]["typecheck"] = f"{run}mypy ."
        elif "pyright" in py_blob or "basedpyright" in py_blob:
            info["commands"]["typecheck"] = f"{run}pyright"
    if "celery" in py_blob:
        add("backend", "Celery")

    # ---- Other backends
    if (root / "go.mod").exists():
        add("backend", "Go")
        info["commands"].setdefault("go_test", "go test ./...")
    if (root / "Cargo.toml").exists():
        add("backend", "Rust")
        info["commands"].setdefault("rust_test", "cargo test --workspace")
        info["commands"].setdefault("rust_lint", "cargo clippy --workspace --all-targets -- -D warnings")

    # ---- JavaScript / TypeScript
    pkg_path = root / "package.json"
    if pkg_path.exists():
        pm = (
            "pnpm"
            if (root / "pnpm-lock.yaml").exists()
            else "yarn"
            if (root / "yarn.lock").exists()
            else "bun"
            if (root / "bun.lock").exists() or (root / "bun.lockb").exists()
            else "npm"
        )
        add("frontend", f"Node ({pm})")
        try:
            data = json.loads(pkg_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        for dep, label in (
            ("next", "Next.js"),
            ("react", "React"),
            ("vue", "Vue"),
            ("nuxt", "Nuxt"),
            ("astro", "Astro"),
            ("@sveltejs/kit", "SvelteKit"),
            ("@remix-run/react", "Remix"),
            ("vite", "Vite"),
            ("typescript", "TypeScript"),
            ("@nestjs/core", "NestJS"),
            ("express", "Express"),
        ):
            if dep in deps:
                add("frontend" if label not in ("NestJS", "Express") else "backend", label)
        if "prisma" in deps or "@prisma/client" in deps:
            add("database", "Prisma")
        if "drizzle-orm" in deps:
            add("database", "Drizzle")
        info["seo_surface"] = any(
            d in deps for d in ("next", "nuxt", "astro", "@sveltejs/kit", "@remix-run/react", "gatsby")
        )
        scripts = data.get("scripts", {})
        runner = "npm run" if pm == "npm" else pm
        for script, key in (
            ("lint", "fe_lint"),
            ("test", "fe_test"),
            ("build", "fe_build"),
            ("typecheck", "fe_typecheck"),
        ):
            if script in scripts:
                info["commands"][key] = f"{runner} {script}"
        if "typescript" in deps and "fe_typecheck" not in info["commands"]:
            info["commands"]["fe_typecheck"] = f"{'npx' if pm == 'npm' else pm + ' exec'} tsc --noEmit"
        info["commands"].setdefault(
            "fe_install",
            {
                "pnpm": "pnpm install --frozen-lockfile",
                "yarn": "yarn install --immutable",
                "bun": "bun install --frozen-lockfile",
                "npm": "npm ci",
            }[pm],
        )

    # ---- Mobile / games
    if any(n.startswith("build.gradle") for n in names) or "AndroidManifest.xml" in names:
        add("mobile", "Android")
        if any(f.suffix == ".kt" for f in files):
            add("mobile", "Kotlin")
        info["commands"].setdefault("android_test", "./gradlew test")
        info["commands"].setdefault("android_assemble", "./gradlew :app:assembleDebug")
        info["commands"].setdefault("android_lint", "./gradlew lint")
    if (root / "ProjectSettings" / "ProjectVersion.txt").exists() or (
        (root / "Assets").is_dir() and any(f.suffix == ".unity" for f in files)
    ):
        add("mobile", "Unity")
    if (root / "project.godot").exists():
        add("mobile", "Godot")
    if (root / "pubspec.yaml").exists():
        add("mobile", "Flutter")

    # ---- Containers / CI
    compose_files = [f for f in files if re.fullmatch(r"(docker-)?compose(\.[\w-]+)?\.ya?ml", f.name)]
    info["docker"] = bool(compose_files) or "Dockerfile" in names
    if (root / ".github" / "workflows").is_dir():
        add("ci", "GitHub Actions")
    if (root / ".gitlab-ci.yml").exists():
        add("ci", "GitLab CI")
    if (root / ".github" / "dependabot.yml").exists() or (root / "renovate.json").exists():
        add("ci", "Dependency bot")

    # ---- Datastores (dependency manifests + compose images)
    blob = (py_blob + text(pkg_path) + "".join(text(f) for f in compose_files)).lower()
    for needle, label in (
        ("postgres", "PostgreSQL"),
        ("psycopg", "PostgreSQL"),
        ("pgvector", "pgvector"),
        ("redis", "Redis"),
        ("valkey", "Valkey"),
        ("mysql", "MySQL"),
        ("mariadb", "MariaDB"),
        ("mongo", "MongoDB"),
        ("sqlite", "SQLite"),
        ("shahrah", "shahrah (geo-sharding proxy)"),
        ("pgbouncer", "PgBouncer"),
    ):
        if needle in blob:
            add("database", label)

    # ---- MCP servers configured for any agent
    for cfg in (".mcp.json", ".cursor/mcp.json", ".vscode/mcp.json", ".codex/config.toml"):
        p = root / cfg
        if p.exists():
            info["mcp"].append({"file": cfg, "servers": mcp_servers(text(p), toml=cfg.endswith(".toml"))})

    # ---- Public web surface (drives SEO skill)
    if not info["seo_surface"]:
        info["seo_surface"] = any(r.endswith(("index.html", "robots.txt", "sitemap.xml")) for r in rel) or (
            "Django" in info["backend"] and any("templates" in f.parts for f in files)
        )

    if len(info["backend"]) + len(info["frontend"]) + len(info["mobile"]) >= 5:
        info["profile"] = "Large"
    return info


def context_dir(root: Path) -> Path:
    """Prefer vendored rigor-os/project-context; else this repo's project-context."""
    nested = root / "rigor-os" / "project-context"
    if (root / "rigor-os").is_dir():
        return nested
    if (root / "constitution").is_dir() and (root / "skills").is_dir():
        return root / "project-context"
    return nested


def is_pristine(path: Path) -> bool:
    if not path.exists():
        return True
    body = text(path)
    return any(m in body for m in TEMPLATE_MARKERS)


def write(path: Path, content: str, force: bool, dry_run: bool, report: list[str]) -> None:
    if not force and not is_pristine(path):
        report.append(f"kept   {path.name} (edited; use --force to regenerate)")
        return
    report.append(f"wrote  {path.name}")
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def join(items: list, empty: str) -> str:
    return ", ".join(items) or empty


def render(info: dict, os_prefix: str) -> dict[str, str]:
    files: dict[str, str] = {}
    mcp = "; ".join(f"{m['file']} → {', '.join(m['servers']) or '?'}" for m in info["mcp"]) or "none configured"
    files[
        "PROJECT_CONTEXT.md"
    ] = f"""# Project Context (generated by bootstrap.py — edit freely, reruns keep your edits)

## Profile

{info["profile"]}

## Product

_Describe the product in one paragraph._

## Stack

- Backend: {join(info["backend"], "unknown")}
- Frontend / Web: {join(info["frontend"], "unknown")}
- Mobile / Android: {join(info["mobile"], "none detected")}
- Database: {join(info["database"], "unknown")}
- Auth: _fill in_
- Docker: {"yes" if info["docker"] else "no"}
- CI: {join(info["ci"], "none detected")}
- MCP servers: {mcp}
- Public web surface (SEO): {"yes — run tools/seo_context.py" if info["seo_surface"] else "not detected"}
- Model routing: see MODEL_ROUTING.md (T0–T3 → economy/standard/strong/max)

## Repository layout

_Fill module map after first exploration._

## Domain boundaries

_Fill._

## API conventions

Pagination keys: current, page_count, page_size, count, next, previous, results (adjust if different)
Error shape: _match sibling endpoints_
Auth: _fill_

## Critical business rules

_Fill._

## External integrations

_Fill._

## Mobile notes

If Android/game: also fill `MOBILE.md` in this folder (client type, engine, build commands).
"""

    cmds = ["# Commands (generated — edit to match reality)", ""]
    for k, v in info["commands"].items():
        cmds += [f"## {k}", "", "```bash", v, "```", ""]
    if info["docker"]:
        cmds += [
            "## docker",
            "",
            "```bash",
            f"docker compose -f {os_prefix}docker/fullstack/compose.yml up --build",
            "```",
            "",
        ]
    cmds += ["## gates", "", "```bash", f"bash {os_prefix}tools/validate-gates.sh", "```", ""]
    if info["seo_surface"]:
        cmds += ["## seo_context", "", "```bash", f"python3 {os_prefix}tools/seo_context.py --check", "```", ""]
    files["COMMANDS.md"] = "\n".join(cmds)

    files["ARCHITECTURE.md"] = """# Architecture (generated stub — edit freely)

## System map

_Fill after reading the codebase._

## Apps / modules

_Fill._

## Data stores

_Fill. Note pooling (PgBouncer/shahrah), replicas, partitioning, and residency rules._

## Background jobs

_Fill._

## Authn / authz model

_Fill._

## Deployment topology

_Fill._

## Mobile clients

_Fill if Android/game — modules, engines, API base URL config._
"""

    if info.get("mobile"):
        game = any(x in info["mobile"] for x in ("Unity", "Godot"))
        files["MOBILE.md"] = f"""# Mobile / Android Context (generated stub — edit freely)

## Client type

{"Mobile game" if game else "Android app"} — detected: {", ".join(info["mobile"])}

## Engine / UI toolkit

_Fill: Compose / Views / Unity / Godot_

## Architecture

_Mirror existing — MVVM / MVI / Clean / engine layout_

## Commands

See COMMANDS.md (android_* entries if detected).

## Server-authoritative systems (games)

_score, currency, IAP — fill_
"""
    return files


def stack_decision(info: dict) -> str:
    if not (info.get("backend") or info.get("frontend") or info.get("mobile")):
        return """<!-- rigor-os:template — replaced automatically once a stack is detected -->
# Stack Decision

## Status

**No stack detected.** Run skill `stack-selection` / workflow `StackSelection`:
classify project type (web, mobile-game, llm-app, …) and apply
`standards/DefaultStackMatrix.md`. Then fill this file.

## Project type

_pending_

## Chosen stack

_pending_

## Rationale

_pending_
"""
    return f"""# Stack Decision

## Status

Existing stack detected — **do not re-select**.

- Backend: {", ".join(info.get("backend") or ["—"])}
- Frontend / Web: {", ".join(info.get("frontend") or ["—"])}
- Mobile: {", ".join(info.get("mobile") or ["—"])}

Match sibling patterns. See `skills/architecture/StackSelectionSkill.md`.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bootstrap Rigor OS project context")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--force", action="store_true", help="Regenerate files even if you edited them")
    parser.add_argument("--dry-run", action="store_true", help="Detect and report; write nothing")
    parser.add_argument("--json", action="store_true", help="Print detection as JSON only")
    args = parser.parse_args(argv)

    root = find_root(args.root)
    info = detect(root)
    if args.json:
        print(json.dumps(info, indent=2))
        return 0

    pc = context_dir(root)
    os_prefix = "rigor-os/" if pc.parent.name == "rigor-os" and pc.parent != root else ""
    report: list[str] = []
    for name, content in render(info, os_prefix).items():
        write(pc / name, content, args.force, args.dry_run, report)
    write(pc / "STACK_DECISION.md", stack_decision(info), args.force, args.dry_run, report)

    print(f"project-context: {pc}{' (dry run)' if args.dry_run else ''}")
    print("\n".join(f"  {line}" for line in report))
    print(f"Detected: {json.dumps(info, indent=2)}")
    if not (info.get("backend") or info.get("frontend") or info.get("mobile")):
        print("HINT: No stack detected — use stack-selection (standards/DefaultStackMatrix.md) before scaffolding.")
    if info["seo_surface"]:
        print(f"HINT: Public web surface found — run `python3 {os_prefix}tools/seo_context.py` for the SEO agent.")
    if info["mcp"]:
        print("HINT: MCP servers configured — review them with skills/ai/MCPGovernanceSkill.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
