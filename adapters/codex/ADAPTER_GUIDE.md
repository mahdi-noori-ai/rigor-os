# Codex Adapter Guide

| Canonical | Codex |
|-----------|--------|
| L1 | Root `AGENTS.md` (keep lean; default **32 KiB** combined budget) |
| Nested guidance | Nested `AGENTS.md` closer to cwd wins |
| Skills | `.agents/skills/*/SKILL.md` (Agent Skills standard; discovered cwd → repo root) |
| Hooks | `.codex/hooks.json` — `{"hooks": {"PreToolUse": [...]}}`; guard returns `permissionDecision: "deny"` |
| Config | `.codex/config.toml` features / `[mcp_servers.*]` |

Project `.codex/` config and hooks load only after you trust the folder in Codex.

**Critical:** Large root AGENTS.md starves nested files. Keep root under ~8 KiB; put depth in `rigor-os/` and skills.

Install: `bash rigor-os/tools/sync-adapters.sh codex`
