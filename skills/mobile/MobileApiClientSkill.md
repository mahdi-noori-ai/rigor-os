# Skill: Mobile API Client

```
Name: mobile-api-client
Domain: mobile
Purpose: Keep Android/game clients in sync with backend contracts, auth, and offline behavior
Trigger: Retrofit/Ktor/Unity HTTP, API DTO change, token refresh, pagination on mobile, OpenAPI for mobile
Do Not Trigger: Backend-only with no client; CSS-only web
```

## Non-negotiables

1. Treat backend OpenAPI / schemas as source of truth — regenerate or update DTOs with the API change.
2. Auth: interceptors for tokens; refresh once; on 401 clear session and route to login as siblings do.
3. Timeouts, retries (idempotent GETs only), and error mapping to UI states.
4. Never log Authorization headers or PII payloads.
5. Feature incomplete until a real device/emulator call succeeds (or project instrumentation test).

## Procedure

1. Impact-analyze: endpoint → DTO → repository → ViewModel/game service → UI.
2. Update client models to match server (nullability, enums, pagination keys).
3. Handle 400/401/403/404/429/5xx explicitly if siblings do.
4. Pagination: use same keys as backend (`current`, `page_count`, … or project standard).
5. Version headers / `Accept` if the API is versioned.
6. Certificate pinning only if the project already uses it — don't invent without ops support.

## Offline & sync

- Read-through cache when the app already has Room/DataStore patterns.
- Conflict policy: server wins unless product says otherwise.
- Idempotency keys for POSTs that may retry (purchases, rewards claim).

## Anti-patterns

- Silent swallow of network errors
- Parallel refresh-token storms
- Mock-only “integration” with no live call
- Different field names than OpenAPI “for convenience”

## Related

`contract-integrity`, `api-engineer`, `mobile-backend-api`, `android-app`
