# AGENTS.md (Codex — keep lean)

Governed by `rigor-os/`.

1. Match existing codebase / sibling patterns.
2. DONE needs evidence (lint, tests, integration).
3. Smallest correct diff; no skipped tests; no secrets.
4. Prefer ruff/pytest/tsc/schema validation.
5. Load skills under `rigor-os/skills/` as needed.
6. FE+BE: verify real API integration.
7. Django layered: no ORM in services; DI; Ruff; service tests.
8. UI: professional, responsive, reuse design system.
9. Android/game: skills/mobile, server-side economy/IAP, MobileGate.
10. Greenfield/no stack: stack-selection defaults; existing repo stack always wins.
11. Destructive ops require approval.
12. After 3 failed loops → BLOCKED.

See `rigor-os/project-context/COMMANDS.md`, `MOBILE.md` if present, and `constitution/CONSTITUTION.md`.
