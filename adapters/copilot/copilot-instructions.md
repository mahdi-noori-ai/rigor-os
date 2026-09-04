# Copilot repository instructions (Rigor OS)

Follow `rigor-os/` governance.

- Match existing codebase patterns before writing.
- Evidence-based completion (lint/tests).
- Smallest correct diff; never skip tests or commit secrets.
- Prefer project commands from `rigor-os/project-context/COMMANDS.md`.
- For Django layered apps: no ORM in services; repositories + DI; Ruff; service tests.
- For UI: reuse design system; responsive; loading/empty/error states; professional look.
- For API changes: update schema and frontend/mobile types; verify integration.
- For Android/mobile games: match app architecture; server-authoritative score/currency/IAP; MobileGate + device smoke.
