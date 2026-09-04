# Mobile Game Feature Workflow

Use for gameplay, economy, HUD, levels, or game+backend features on Android.

## Flow

```
Define playable acceptance (what the player can do)
    → Separate sim / HUD / network
    → Server authority for economy/score/IAP if online
    → Implement game change
    → Client API + backend validation
    → Performance sanity (no obvious hitch in the new path)
    → Build Android + smoke play
    → MobileGate + SecurityGate if economy/IAP
```

## Implementation order (online game)

1. Backend rules + tests (authoritative)
2. OpenAPI / contract
3. Client network + local optimistic UI if needed
4. Gameplay / HUD
5. Anti-abuse (rate limits, idempotent claims)
6. Device playtest evidence

## Skills

`mobile-game`, engine overlay (`unity-android` or android native), `mobile-backend-api`, `mobile-api-client`, `mobile-ui-ux`, `mobile-security`, `performance`

## Anti-patterns

- Shipping client-only currency
- Mixing network calls into the core update loop without existing pattern
- Skipping IAP server verification
