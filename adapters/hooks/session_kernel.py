#!/usr/bin/env python3
"""SessionStart hook for the Rigor OS Claude Code plugin.

A plugin's CLAUDE.md is never loaded as context, so this hook prints the kernel
(adapters/claude/CLAUDE.md) on stdout — which Claude Code adds to context — with
documentation paths resolved to the installed plugin, plus where this project's
context files live. Stays well under the 10,000-character hook output cap.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

LIMIT = 9000


def render(plugin_root: Path, project: Path) -> str:
    kernel = (plugin_root / "adapters" / "claude" / "CLAUDE.md").read_text(encoding="utf-8")
    kernel = kernel.replace(
        "You operate under `rigor-os/`.", f"Rigor OS is installed as a plugin at `{plugin_root.as_posix()}`."
    )
    kernel = re.sub(r"rigor-os/(?!project-context)", f"{plugin_root.as_posix()}/", kernel)

    context = project / "rigor-os" / "project-context"
    if (context / "PROJECT_CONTEXT.md").exists():
        status = "Project context: `rigor-os/project-context/` (read COMMANDS.md before running tools)."
    else:
        status = (
            "Project context is missing. Before non-trivial work, run:\n"
            f"`python3 {plugin_root.as_posix()}/tools/bootstrap.py --root .`"
        )
    footer = (
        "\n## Plugin paths\n\n"
        f"- `${{CLAUDE_PLUGIN_ROOT}}` in project-context files means `{plugin_root.as_posix()}`.\n"
        f"- Gates: `bash {plugin_root.as_posix()}/tools/validate-gates.sh`\n"
        f"- SEO extractor: `python3 {plugin_root.as_posix()}/tools/seo_context.py`\n"
        f"- {status}\n"
    )
    text = kernel.rstrip() + "\n" + footer
    return text if len(text) <= LIMIT else text[: LIMIT - 40] + "\n…(truncated; see adapters/claude/CLAUDE.md)\n"


def main() -> int:
    sys.stdin.read()  # drain the hook payload; nothing in it is needed
    root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or Path(__file__).resolve().parents[2])
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path.cwd())
    try:
        sys.stdout.write(render(root, project))
    except OSError:
        return 0  # never block a session start
    return 0


if __name__ == "__main__":
    sys.exit(main())
