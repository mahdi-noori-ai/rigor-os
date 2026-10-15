import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import bootstrap  # noqa: E402


def write(base: Path, rel: str, text: str = "") -> None:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def vendored_project(tmp_path: Path) -> Path:
    (tmp_path / "rigor-os" / "project-context").mkdir(parents=True)
    write(tmp_path, "manage.py", "")
    write(
        tmp_path,
        "pyproject.toml",
        '[project]\ndependencies = ["django>=5", "djangorestframework", "psycopg[binary]", "celery"]\n',
    )
    write(tmp_path, "uv.lock", "")
    write(
        tmp_path,
        "package.json",
        json.dumps(
            {
                "dependencies": {"next": "16", "react": "19"},
                "devDependencies": {"typescript": "5"},
                "scripts": {"lint": "next lint", "build": "next build"},
            }
        ),
    )
    write(tmp_path, "pnpm-lock.yaml", "")
    write(
        tmp_path,
        "compose.yaml",
        "services:\n  db:\n    image: postgres:18-alpine\n  cache:\n    image: valkey/valkey:9\n",
    )
    write(tmp_path, ".mcp.json", json.dumps({"mcpServers": {"github": {}, "postgres": {}}}))
    write(tmp_path, "node_modules/pkg/build.gradle", "")  # must be ignored
    return tmp_path


def test_detects_modern_stack(tmp_path):
    info = bootstrap.detect(vendored_project(tmp_path))
    assert {"Django", "DRF", "Celery"} <= set(info["backend"])
    assert {"Next.js", "React", "TypeScript", "Node (pnpm)"} <= set(info["frontend"])
    assert {"PostgreSQL", "Valkey"} <= set(info["database"])
    assert info["mobile"] == [], "node_modules must be pruned"
    assert info["commands"]["test"] == "uv run pytest"
    assert info["commands"]["fe_lint"] == "pnpm lint"
    assert info["commands"]["fe_install"] == "pnpm install --frozen-lockfile"
    assert info["mcp"] == [{"file": ".mcp.json", "servers": ["github", "postgres"]}]
    assert info["seo_surface"] is True
    assert info["docker"] is True


def test_rerun_keeps_user_edits(tmp_path):
    root = vendored_project(tmp_path)
    pc = root / "rigor-os" / "project-context"
    assert bootstrap.main(["--root", str(root)]) == 0
    ctx = pc / "PROJECT_CONTEXT.md"
    assert "Django" in ctx.read_text()
    assert "seo_context.py" in (pc / "COMMANDS.md").read_text()

    ctx.write_text(ctx.read_text().replace("_Describe the product in one paragraph._", "Acme sells widgets."))
    bootstrap.main(["--root", str(root)])
    assert "Acme sells widgets." in ctx.read_text()

    bootstrap.main(["--root", str(root), "--force"])
    assert "Acme sells widgets." not in ctx.read_text()


def test_shipped_templates_are_replaced(tmp_path):
    root = vendored_project(tmp_path)
    pc = root / "rigor-os" / "project-context"
    for name in ("PROJECT_CONTEXT.md", "COMMANDS.md", "STACK_DECISION.md"):
        (pc / name).write_text((ROOT / "project-context" / name).read_text())
    bootstrap.main(["--root", str(root)])
    assert "Existing stack detected" in (pc / "STACK_DECISION.md").read_text()
    assert "uv run pytest" in (pc / "COMMANDS.md").read_text()


def test_dry_run_writes_nothing(tmp_path):
    root = vendored_project(tmp_path)
    bootstrap.main(["--root", str(root), "--dry-run"])
    assert not any((root / "rigor-os" / "project-context").iterdir())


def test_empty_repo_hints_stack_selection(tmp_path, capsys):
    (tmp_path / "rigor-os").mkdir()
    bootstrap.main(["--root", str(tmp_path)])
    assert "No stack detected" in capsys.readouterr().out
    text = (tmp_path / "rigor-os" / "project-context" / "STACK_DECISION.md").read_text()
    assert "rigor-os:template" in text
