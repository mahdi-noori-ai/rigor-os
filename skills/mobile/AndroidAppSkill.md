# Skill: Android App

```
Name: android-app
Domain: mobile
Purpose: Build and change Android apps with production structure, not ad-hoc Activities
Trigger: Android / Kotlin / Jetpack Compose / Gradle / APK / Play feature work
Do Not Trigger: Pure backend-only with no client change; iOS-only; web-only
```

## Non-negotiables

1. Match the existing app architecture (MVVM, MVI, Clean, modularization) before inventing a new one.
2. Reuse existing modules, navigation, DI, networking, and design tokens/theme.
3. UI must handle loading / empty / error / offline — not happy-path only.
4. Never hardcode secrets, API keys, or signing passwords in source.
5. New screens must work on small phones and common tablets (or document phone-only).
6. Run the project's Gradle checks (`./gradlew lint`, unit tests) before DONE.

## Recommended structure (adapt to repo)

```
app/                 # application module
feature-<name>/      # feature modules when the project already modularizes
core-ui/             # shared Compose/XML components
core-network/        # API client, interceptors, DTOs
core-data/           # repositories, local DB (Room)
core-domain/         # use cases / models (if Clean/layered)
```

If the project is a single `app` module, keep features in packages mirroring siblings — do not force multi-module without need.

### Responsibilities

| Layer | May do | Must not do |
|-------|--------|-------------|
| UI (Compose/Fragment) | Collect state, render, navigate, user events | Business rules, raw HTTP, DB |
| ViewModel | UI state, call use cases/repos, map errors | Android framework views, long blocking work on main |
| Domain / UseCase | Rules, orchestration | Android imports when project isolates them |
| Data / Repository | Network + local source of truth | UI logic |
| Network | Retrofit/Ktor, mappers, auth headers | Business policy |

## Workflow

1. Find a sibling feature screen/module; copy package layout and naming.
2. Define UI states explicitly (`Loading`, `Content`, `Empty`, `Error`).
3. Wire navigation the same way as siblings (Compose Nav / Fragments).
4. Add/extend repository + API DTO; keep contract aligned with backend OpenAPI.
5. Persist only what siblings persist (DataStore/Room patterns).
6. Unit-test ViewModel/use case; instrumented/UI tests when the project already uses them.
7. `./gradlew :app:assembleDebug` (or project equivalent) must succeed for the change.

## Configuration & flavors

- Use `BuildConfig` / `local.properties` / CI secrets for base URLs — not committed `.env` with production keys.
- Debug vs release: logging off or redacted in release; minify rules updated if ProGuard/R8 strips needed classes.

## Anti-patterns

- Business logic in Composables/Activities
- Ignoring configuration changes / process death when siblings handle them
- Blocking main thread with network/disk
- New DI framework when Hilt/Koin already exists
- Shipping `TODO` network stubs as production behavior
- Ignoring RTL / accessibility labels on interactive controls

## Related

`mobile-api-client`, `mobile-ui-ux`, `mobile-testing`, `mobile-security`, `mobile-release`, overlays `android-kotlin`
