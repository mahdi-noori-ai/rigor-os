# Claude Code Adapter Guide

| Canonical | Claude Code |
|-----------|-------------|
| L1 Constitution | `CLAUDE.md` |
| Skills | `.claude/skills/*/SKILL.md` (description auto-invoke) |
| Review agents | `.claude/agents/*.md` — `model: opus`, `effort`, `permissionMode: plan`, `disallowedTools` keep reviewers read-only |
| SEO agent | `.claude/agents/seo-strategist.md` (opt-in) |
| Hooks | `.claude/settings.json` → `PreToolUse` runs `.claude/hooks/guard_shell.py` (returns `hookSpecificOutput.permissionDecision: "deny"`) |
| Permissions | `deny` for secret files (`Read(.env)` …) and force-push; `ask` for `git push`, dependency installs — deny always beats allow |
| MCP | `.mcp.json` — start from `templates/mcp.json.example` |

Hooks are deterministic; a `PreToolUse` deny blocks even under permissive modes. `.env.example` stays readable
because deny rules list concrete secret files rather than `.env.*`.

Install, either:

- **Plugin:** `/plugin marketplace add mahdi-noori-ai/rigor-os` then `/plugin install rigor-os@rigor-os`. The marketplace
  entry in `.claude-plugin/marketplace.json` is the manifest: it lists `adapters/skills/` and the three agents (so the
  root `skills/` and `agents/` doc folders are never scanned), a `SessionStart` hook that prints the kernel
  (`adapters/hooks/session_kernel.py` — plugin `CLAUDE.md` files are not loaded), and the guard hook. Skills and agents
  reference docs as `${CLAUDE_PLUGIN_ROOT}/…`. Permission rules cannot ship in a plugin.
- **Vendored:** `bash rigor-os/tools/sync-adapters.sh claude` — copies the same files and rewrites
  `${CLAUDE_PLUGIN_ROOT}` to the path of `rigor-os/` in your project.
