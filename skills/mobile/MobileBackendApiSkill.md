# Skill: Mobile Backend API (for apps & games)

```
Name: mobile-backend-api
Domain: backend / mobile
Purpose: Design backend APIs that mobile and game clients can rely on
Trigger: APIs for Android/game clients, push, IAP verify, leaderboards, sessions, device tokens, app version gates
Do Not Trigger: Admin-only web internal tools with no mobile consumer
```

## Non-negotiables

1. Same layering/DI/tests as the rest of the backend (Django overlay when applicable).
2. **Do not trust the client** for balances, scores, entitlements, or match results.
3. Mobile-friendly errors: stable machine codes + human messages; avoid HTML error pages.
4. Auth suitable for mobile (token/session refresh documented); object-level auth on player resources.
5. Pagination and payload size fit mobile networks; avoid huge nested dumps.
6. Contract + mobile client updated together (`contract-integrity`).

## Mobile/game endpoint patterns

| Feature | Backend must |
|---------|----------------|
| Profile / inventory | Owner checks (BOLA) |
| Leaderboard submit | Validate score bounds, rate-limit, optional replay/signature |
| Claim reward / daily | Idempotent; one claim per period |
| IAP | Verify Play purchase token server-side; grant once |
| Device push token | Upsert per user/device; auth required |
| Force update | `min_app_version` / soft vs hard gate endpoint or config |
| Guest → registered | Merge policy documented; no data loss surprises |

## API design for mobile

- Prefer additive OpenAPI changes; version or coordinate app release for breaking changes.
- Support sparse clients: optional fields, default-safe.
- Compress-friendly JSON; consider ETag/If-None-Match when siblings use caching.
- Time: UTC ISO-8601; document timezone assumptions for dailies.
- Rate-limit abuse-prone routes (login, OTP, reward, leaderboard).

## Push notifications

- Store tokens separately from auth credentials.
- Prefer async job for fan-out.
- No PII in notification bodies beyond product need.

## Anti-patterns

- “Client sent newBalance=99999” accepted
- Breaking JSON rename without app coordinated release
- Unbounded list endpoints for inventory/history
- IAP grant without store verification

## Related

`api-engineer`, `contract-integrity`, `appsec-review`, `mobile-game`, `android-app`
