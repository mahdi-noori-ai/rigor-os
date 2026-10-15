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

Install: `bash rigor-os/tools/sync-adapters.sh claude`
