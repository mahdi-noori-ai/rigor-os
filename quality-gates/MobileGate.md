# Mobile Gate

Apply when Android app or mobile game client code changes (and when backend serves only mobile/game clients for that task).

## Client (Android / game)

- [ ] Follows sibling module/package architecture
- [ ] Loading / empty / error / offline (or reconnect) handled for user-facing flows
- [ ] No secrets in source; release logging safe
- [ ] `assembleDebug` (or project release smoke) succeeds
- [ ] Unit tests for new ViewModel / use case / game rules
- [ ] Touched UI checked on a phone-sized emulator or device
- [ ] Back navigation / pause-resume does not break the feature
- [ ] RTL / font scale: no obvious breakage for app UI (games: document fixed HUD if intentional)

## Client ↔ Backend

- [ ] DTOs match OpenAPI / server
- [ ] Auth errors route correctly
- [ ] Real network call evidence (not mock-only) for integration claims
- [ ] Pagination / error shapes match backend

## Games (extra)

- [ ] Economy / score / IAP not client-authoritative when online services exist
- [ ] New gameplay path playable without crash in smoke session
- [ ] No debug cheat menu in release variant

## Backend for mobile (when API changed)

- [ ] Object-level auth on player resources
- [ ] Idempotent claim/reward/purchase grant where applicable
- [ ] Rate limits considered on abuse-prone routes
- [ ] Contract updated; mobile client updated or version gate documented

## Fail the gate if

- Hardcoded production keys
- “Works in editor” only with no Android build for store-facing client changes
- Trusting client-submitted balances/scores without server checks
