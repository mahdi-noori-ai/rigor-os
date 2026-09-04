# Overlay: Android Kotlin / Jetpack

Use with `android-app` when the project is Kotlin + Gradle Android.

## Defaults (override with sibling code)

- Language: Kotlin
- UI: Jetpack Compose if the app already uses it; else XML/Views as siblings
- DI: Hilt or Koin — never both new
- Async: coroutines + Flow as existing
- Network: Retrofit/OkHttp or Ktor as existing
- Local: Room / DataStore as existing
- Lint: Android Lint + detekt/ktlint if configured

## Gradle

- Version catalogs (`libs.versions.toml`) if present — add deps there
- Don't bump AGP/Kotlin casually without need
- Prefer `implementation` over `api` unless exposing types

## Commands (typical — prefer project-context/COMMANDS.md)

```bash
./gradlew lint
./gradlew test
./gradlew :app:assembleDebug
./gradlew :app:installDebug
```
