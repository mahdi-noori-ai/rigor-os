# Definition of Done

Completion is **contextual**. Do not force irrelevant checks onto every task. Consult `QualityGateMatrix.md` for which items apply.

## Core (Always)

- [ ] Original user requirement fulfilled
- [ ] Acceptance criteria fulfilled (or explicitly agreed if ambiguous)
- [ ] Implementation follows existing architecture and sibling patterns
- [ ] Diff is focused — no unrelated modifications
- [ ] No leaked secrets, credentials, or debug leftover
- [ ] No unresolved TODOs created by this change
- [ ] No unnecessary files added
- [ ] Lint/format passes on changed files (or project equivalent)

## Backend (When Backend Changed)

- [ ] Views thin; business logic in services/use cases
- [ ] ORM queries in repositories, not services (if project uses layered architecture)
- [ ] Request/response shapes match sibling endpoints
- [ ] Service tests added/updated for new or changed services
- [ ] Relevant unit/integration tests pass
- [ ] Authorization checked on new/changed endpoints

## Frontend (When Frontend Changed)

- [ ] Works at mobile, tablet, and desktop widths
- [ ] Loading, empty, error, and success states implemented
- [ ] Forms validate and show errors
- [ ] Keyboard navigable; semantic HTML
- [ ] UI matches existing design system / sibling components (not a one-off robotic layout)
- [ ] API client/types updated if API changed

## Mobile / Android (When App or Game Client Changed)

- [ ] Matches existing Android/game architecture (modules, DI, navigation, engine layout)
- [ ] Loading / empty / error / offline or reconnect states for user-facing flows
- [ ] Touch-first UI or readable HUD; no desktop-only layout
- [ ] Debug build assembles; smoke on emulator/device for the feature
- [ ] Unit tests for new ViewModels, use cases, or game rules
- [ ] API DTOs synced with backend if contract changed
- [ ] No secrets/keystores in the diff; release logging safe
- [ ] Games: server authority for score/currency/IAP when online services exist
- [ ] `MobileGate` checklist completed

## Integration (When Frontend + Backend)

- [ ] Real request/response verified (not mock-only)
- [ ] OpenAPI/schema updated
- [ ] Frontend types/client regenerated or manually synced
- [ ] Auth/permissions behavior verified end-to-end
- [ ] Failure paths tested (4xx/5xx, network error)

## Database (When Schema/Migration Changed)

- [ ] Migration reviewed for production safety
- [ ] Rollback strategy documented
- [ ] Indexes and constraints considered
- [ ] Backward compatible if rolling deploy
- [ ] Destructive operations require explicit approval

## Security (When Security Surface Changed)

- [ ] SecurityGate checklist completed
- [ ] No object-level authorization gaps
- [ ] Input validated
- [ ] Secrets not in code or logs

## Performance (When Data Volume or Hot Path)

- [ ] No obvious N+1 queries
- [ ] Pagination used for lists
- [ ] Evidence-based (do not optimize prematurely)

## Observability (When New Failure Modes)

- [ ] Structured logs on error paths
- [ ] Correlation/request IDs if project already uses them

## Documentation (When Behavior/Setup Changes)

- [ ] README/COMMANDS updated if commands changed
- [ ] API docs updated if public API changed
- [ ] ADR created if significant architectural decision

## Deployment (When Deploy Impact)

- [ ] Migration/deploy order understood
- [ ] Rollback considered
- [ ] Health checks still valid

## Evidence Requirement

DoD is not a checkbox of claims. Attach evidence:

```
Lint: ruff check src/apps/users/  → 0 errors
Tests: pytest apps/users -q  → 24 passed
Contract: openapi types regenerated, no drift
UI: verified at 375px, 768px, 1280px
```

If any required item cannot be verified, report BLOCKED — never false success.
