# Overlay: Unity → Android

Use with `mobile-game` when the client is Unity exporting to Android.

## Non-negotiables

1. Match existing assembly definitions, folder layout, and service patterns.
2. Android plugins / Gradle template changes go through existing `Plugins/Android` or Project Settings flow.
3. IL2CPP + ARM64 as store requires; don't drop architectures casually.
4. PlayerPrefs for tiny flags only — economy stays server-authoritative when online.
5. Test an Android build (or at least Android player) before DONE on store-facing changes.

## Typical structure

```
Assets/_Project/Gameplay/
Assets/_Project/UI/
Assets/_Project/Services/   # IAP, ads, analytics
Assets/_Project/Network/
```

## Build

Document keystore and bundle id in project-context; never commit secrets.
Play Asset Delivery / Addressables: follow existing remote catalog setup.

## Related

`mobile-game`, `mobile-backend-api`, `mobile-release`
