# Cursor Adapter Guide

## Mapping

| Canonical | Cursor |
|-----------|--------|
| Constitution L1 | `AGENTS.md` + `rules/constitution.mdc` (`alwaysApply: true`) |
| Safety | `rules/safety.mdc` + `hooks.json` `beforeShellExecution` → `.cursor/hooks/guard_shell.py` (`failClosed: true`) |
| SEO | `rules/seo.mdc` (globs on pages/layouts) + skill `seo-context` |
| Path rules | `rules/python-backend.mdc`, `rules/frontend.mdc`, `rules/android.mdc` (`globs`) |
| Skills L3 | `.cursor/skills/*/SKILL.md` (`description` triggers; Cursor also reads `.agents/skills`, `.claude/skills`) |
| Workflows | Skills that point at `rigor-os/workflows/*` |
| Review agents | Task/subagents using agent specs; bind to **max** model when UI allows |
| Model routing | Fill `project-context/MODEL_ROUTING.md`; announce `Routing: T#…`; T0 avoid max |
| Hooks | `.cursor/hooks.json` |

## Install

```bash
bash rigor-os/tools/sync-adapters.sh cursor
```

Map `economy` / `standard` / `strong` / `max` in `MODEL_ROUTING.md` to your Cursor model picker names.

## What cannot map identically

- Claude-only permission modes / PreToolUse JSON schema differs slightly from Cursor hook payload.
- Codex 32 KiB AGENTS.md budget — Cursor AGENTS.md can be longer but keep lean for tokens.
- Copilot path instructions use `applyTo` not `globs`.
- Not every UI exposes per-subagent model IDs — still enforce **context budgets** by tier.

Keep **canonical** content in `rigor-os/`; adapters are projections.
