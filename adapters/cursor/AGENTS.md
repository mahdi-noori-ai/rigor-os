# AGENTS.md — Rigor OS (Cursor / portable kernel)

You are governed by the Rigor OS in `rigor-os/`.

## Non-negotiables

1. **Match existing codebase** — find a sibling feature; mirror layout, naming, DI, response shapes.
2. **Evidence-based completion** — lint/tests/integration evidence before DONE; never false success.
3. **Smallest correct diff** — no drive-by refactors.
4. **Deterministic over prose** — run Ruff/pytest/tsc/schema tools.
5. **Safe autonomy** — no destructive production ops, secrets, or irreversible migrations without approval.

## How to work

1. Read `rigor-os/project-context/PROJECT_CONTEXT.md` and `COMMANDS.md`.
2. Select a workflow under `rigor-os/workflows/`.
3. Load matching skills under `rigor-os/skills/` (or Cursor `.cursor/skills/`).
4. Implement → verify → fix (max 3 loops) → Definition of Done.
5. For auth/user-data: SecurityGate + consider Security Reviewer.
6. For FE+BE: IntegrationVerification required.

## Django/DRF projects using clean architecture

Follow `rigor-os/skills/backend/overlays/django-clean-architecture/DjangoCleanArchSkill.md`: ORM-free services, DI interfaces, Ruff, service tests.

## UI

Professional UI required — reuse design tokens; reject robotic default layouts. Responsive + a11y for UI features.

## Mobile / Android / games

When the project is Android or a mobile game, load `rigor-os/skills/mobile/` and workflows `MobileFeature` / `MobileGameFeature`. Prefer server authority for score, currency, and IAP. Fill `project-context/MOBILE.md`. Use `MobileGate` before DONE.

## Stack selection

If there is **no existing stack** and the user did not name one, run `stack-selection` (`standards/DefaultStackMatrix.md`): pick web/mobile/game/LLM defaults, write `STACK_DECISION.md`, then build. Never override an existing repo stack.

## Docker

Prefer `rigor-os/docker/fullstack/` for easy bring-up.
