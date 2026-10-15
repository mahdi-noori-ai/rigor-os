"""Structural checks for the Claude Code plugin marketplace (.claude-plugin/marketplace.json)."""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import bootstrap  # noqa: E402

MARKETPLACE = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
ENTRY = MARKETPLACE["plugins"][0]
TOKEN = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+)")


def plugin_markdown():
    files = []
    for d in ENTRY["skills"]:
        files += sorted((ROOT / d).glob("*/SKILL.md"))
    files += [ROOT / a for a in ENTRY["agents"]]
    return files


def test_marketplace_shape():
    assert MARKETPLACE["name"] == "rigor-os"
    assert MARKETPLACE["owner"]["name"]
    assert ENTRY["name"] == "rigor-os"
    assert ENTRY["source"] == "./"
    assert not (ROOT / ".claude-plugin" / "plugin.json").exists(), (
        "the entry is the manifest; a plugin.json would re-enable the default skills/ scan"
    )


def test_component_paths_exist_and_stay_inside():
    for path in [*ENTRY["skills"], *ENTRY["agents"]]:
        assert path.startswith("./") and ".." not in path, path
        assert (ROOT / path).exists(), path
    for agent in ENTRY["agents"]:
        assert agent.endswith(".md")


def test_no_default_component_folders_load_by_accident():
    # agents/ and skills/ at the root hold canonical docs; the entry's lists replace those scans.
    for name in ("commands", "hooks/hooks.json", ".mcp.json", ".lsp.json", "bin", "settings.json", "CLAUDE.md"):
        assert not (ROOT / name).exists(), f"{name} at the repo root would load into the plugin"


def test_skills_follow_agent_skills_format():
    skills = sorted((ROOT / "adapters" / "skills").glob("*/SKILL.md"))
    assert len(skills) >= 18
    for f in skills:
        head = f.read_text().split("---")[1]
        assert re.search(rf"^name: {f.parent.name}$", head, re.M), f
        assert re.search(r"^description: .{40,}", head, re.M), f


def test_hook_commands_point_at_real_scripts():
    for event, groups in ENTRY["hooks"].items():
        for group in groups:
            for hook in group["hooks"]:
                m = re.search(r'"\$\{CLAUDE_PLUGIN_ROOT\}"/(\S+)', hook["command"])
                assert m, (event, hook["command"])
                assert (ROOT / m.group(1)).is_file(), m.group(1)


def test_plugin_content_resolves_through_plugin_root():
    for f in plugin_markdown():
        text = f.read_text()
        stale = [m for m in re.findall(r"rigor-os/[\w./-]+", text) if not m.startswith("rigor-os/project-context")]
        assert not stale, f"{f}: use ${{CLAUDE_PLUGIN_ROOT}} for {stale}"
        for ref in TOKEN.findall(text):
            ref = ref.rstrip(".")
            assert (ROOT / ref).exists(), f"{f}: missing {ref}"


def test_session_kernel_output(tmp_path):
    env = {**os.environ, "CLAUDE_PLUGIN_ROOT": str(ROOT), "CLAUDE_PROJECT_DIR": str(tmp_path)}
    out = subprocess.run(
        [sys.executable, str(ROOT / "adapters" / "hooks" / "session_kernel.py")],
        input="{}",
        capture_output=True,
        text=True,
        env=env,
        check=True,
    ).stdout
    assert len(out) < 10_000, "SessionStart output is capped at 10,000 characters"
    assert "Evidence-based DONE" in out
    assert f"installed as a plugin at `{ROOT.as_posix()}`" in out
    assert f"{ROOT.as_posix()}/tools/bootstrap.py --root ." in out
    relative = out.replace(ROOT.as_posix(), "<plugin>")
    assert not [m for m in re.findall(r"rigor-os/[\w./-]+", relative) if not m.startswith("rigor-os/project-context")]

    (tmp_path / "rigor-os" / "project-context").mkdir(parents=True)
    (tmp_path / "rigor-os" / "project-context" / "PROJECT_CONTEXT.md").write_text("x")
    out = subprocess.run(
        [sys.executable, str(ROOT / "adapters" / "hooks" / "session_kernel.py")],
        input="{}",
        capture_output=True,
        text=True,
        env=env,
        check=True,
    ).stdout
    assert "Project context: `rigor-os/project-context/`" in out


def test_bootstrap_prefix_for_each_layout(tmp_path):
    assert bootstrap.os_prefix(tmp_path, tmp_path / "rigor-os") == "rigor-os/"
    assert bootstrap.os_prefix(tmp_path, tmp_path) == ""
    assert bootstrap.os_prefix(tmp_path, ROOT) == "${CLAUDE_PLUGIN_ROOT}/"


def test_sync_renders_plugin_paths_for_vendored_installs(tmp_path):
    vendored = tmp_path / "rigor-os"
    shutil.copytree(ROOT, vendored, ignore=shutil.ignore_patterns(".git", ".venv", "*cache*"))
    subprocess.run(["bash", str(vendored / "tools" / "sync-adapters.sh"), "claude"], check=True, capture_output=True)
    for f in [*(tmp_path / ".claude" / "skills").glob("*/SKILL.md"), *(tmp_path / ".claude" / "agents").glob("*.md")]:
        text = f.read_text()
        assert "CLAUDE_PLUGIN_ROOT" not in text, f
        for ref in re.findall(r"`(rigor-os/[\w./-]+?)`", text):
            if not ref.startswith("rigor-os/project-context"):
                assert (tmp_path / ref).exists(), f"{f}: {ref}"
