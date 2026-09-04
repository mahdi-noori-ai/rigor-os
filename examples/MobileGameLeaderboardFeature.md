# Example: Android game + Django backend — daily reward & leaderboard

## User request

> Build a mobile game daily reward claim and leaderboard on Android, with Django API, auth, validation, and anti-cheat basics.

## Orchestrator summary

| Decision | Choice |
|----------|--------|
| Workflows | MobileGameFeature + backend FeatureImplementation slice |
| Domains | Backend, DB, API contract, Android/game client, Security |
| Skills | mobile-game, mobile-backend-api, django-clean-architecture, contract-integrity, mobile-api-client, mobile-security, mobile-testing |
| Reviewer | SecurityReviewer (rewards + leaderboard authz) |

## Task order

1. **Backend:** `ClaimDailyReward` + `SubmitScore` / `ListLeaderboard` — ORM-free services, repos, object-level auth.
2. **Rules:** one claim per UTC day (idempotent); score bounds + rate limit; never accept `newBalance` from client.
3. **Migration** if new tables (reward_claims, scores).
4. **OpenAPI / schemas.py** + tests (401/403/400/200, double-claim).
5. **Android/game client:** DTO + repository + UI/HUD buttons; handle already-claimed and offline.
6. **Integration:** real HTTP from emulator against local Docker API.
7. **MobileGate + SecurityGate + DoD.**

## Evidence example

```
pytest apps/game -q → passed
ruff check → clean
./gradlew :app:assembleDebug → success
emulator: claim once → 200; claim again → 409/400; leaderboard shows server score
SecurityReviewer: PASS (no client-trusted balance)
```
