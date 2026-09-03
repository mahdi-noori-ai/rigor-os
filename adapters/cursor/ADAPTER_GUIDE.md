# Cursor Adapter Guide

## Mapping

| Canonical | Cursor |
|-----------|--------|
| Constitution L1 | `AGENTS.md` + `rules/constitution.mdc` (`alwaysApply: true`) |
| Safety | `rules/safety.mdc` + `hooks.json` `beforeShellExecution` |
| Path rules | `rules/python-backend.mdc`, `rules/frontend.mdc` (`globs`) |
| Skills L3 | `.cursor/skills/*/SKILL.md` (`description` triggers) |
| Workflows | Skills that point at `rigor-os/workflows/*` |
| Review agents | Cursor Task/subagents or manual review using agent specs |
| Hooks | `.cursor/hooks.json` |

## Install

```bash
bash rigor-os/tools/sync-adapters.sh cursor
```

## What cannot map identically

- Claude-only permission modes / PreToolUse JSON schema differs slightly from Cursor hook payload.
- Codex 32 KiB AGENTS.md budget — Cursor AGENTS.md can be longer but keep lean for tokens.
- Copilot path instructions use `applyTo` not `globs`.

Keep **canonical** content in `rigor-os/`; adapters are projections.
