# Skill: Mobile Testing

```
Name: mobile-testing
Domain: mobile / testing
Purpose: Right-sized tests for Android apps and games
Trigger: New ViewModels, use cases, game rules, API clients, UI flows on Android
Do Not Trigger: Docs-only
```

## Hierarchy

| Level | Examples | When |
|-------|----------|------|
| Unit | ViewModel, use case, pure game rules | Always for new logic |
| Integration | Repository + fake API / Room | Persistence & networking |
| Instrumented | Espresso / Compose UI / game smoke scene | Critical flows Medium+ |
| Contract | Client DTO vs OpenAPI | API changes |
| Device smoke | Install debug APK, open feature | Before claiming UI done |

## Rules

1. Prefer testing game rules and ViewModels without the Android framework when possible.
2. Don't replace failing UI tests with Thread.sleep flakiness — use idling / waits project already uses.
3. IAP and billing: use official test tracks / fakes; never charge real money in automated tests.
4. Screenshot/visual tests only if the project already has them.

## Evidence

Paste `./gradlew test` (and instrumented if required) outputs. For games: “scene X loads, action Y works on emulator” with build flavor noted.

## Related

`test-strategy`, `flaky-test-investigation`, `android-app`, `mobile-game`
