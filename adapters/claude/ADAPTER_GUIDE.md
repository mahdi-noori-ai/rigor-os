# Claude Code Adapter Guide

| Canonical | Claude Code |
|-----------|-------------|
| L1 Constitution | `CLAUDE.md` |
| Skills | `.claude/skills/*/SKILL.md` (description auto-invoke) |
| Review agents | `.claude/agents/*.md` |
| Hooks | `.claude/settings.json` → `hooks` (`PreToolUse`, `PostToolUse`, `Stop`) |
| Permissions | `permissions.allow` / `deny` in settings — model instructions cannot override |

Hooks are deterministic; use `PreToolUse` to deny destructive Bash even under permissive modes.

Install: `bash rigor-os/tools/sync-adapters.sh claude`
