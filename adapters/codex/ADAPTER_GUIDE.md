# Codex Adapter Guide

| Canonical | Codex |
|-----------|--------|
| L1 | Root `AGENTS.md` (keep lean; default **32 KiB** combined budget) |
| Nested guidance | Nested `AGENTS.md` closer to cwd wins |
| Hooks | `.codex/hooks.json` (`PreToolUse`, `Stop`, …) |
| Config | `.codex/config.toml` permissions / MCP |

**Critical:** Large root AGENTS.md starves nested files. Keep root under ~8 KiB; put depth in `rigor-os/` and skills.

Install: `bash rigor-os/tools/sync-adapters.sh codex`
