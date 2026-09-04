# CLAUDE.md — Rigor OS

You operate under `rigor-os/`.

## Rules

1. Match existing codebase; mirror siblings.
2. Evidence-based DONE (lint/tests/integration).
3. Smallest correct diff.
4. Prefer tools (ruff, pytest, tsc, gradle) over claims.
5. No secrets; no skipping tests; no destructive ops without approval.
6. Load skills when relevant; do not load entire handbook.
7. FE+BE requires IntegrationVerification.
8. Django layered apps: ORM-free services + DI + Ruff + service tests (`skills/backend/overlays/django-clean-architecture/`).
9. UI must be professional and responsive — not robotic defaults.
10. Android/mobile game: `skills/mobile/`, server-authoritative economy/IAP, `MobileGate`, device/build smoke.
11. After 3 failed fix loops → BLOCKED with evidence.

Read `rigor-os/project-context/COMMANDS.md` (and `MOBILE.md` if present) before inventing commands.
Workflows: `rigor-os/workflows/`. Gates: `rigor-os/quality-gates/`.
