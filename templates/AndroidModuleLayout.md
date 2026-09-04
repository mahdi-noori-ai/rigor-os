# Android Module Layout (reference)

Use only as a starting map when the repo has no strong structure yet. Prefer existing layout.

```
app/
  src/main/java/.../app/          # Application, nav host
  src/main/java/.../feature/x/    # UI + ViewModel for feature x (if single-module)
core/
  network/                        # API, DTOs, interceptors
  data/                           # repositories, Room
  domain/                         # use cases (optional)
  ui/                             # shared components, theme
feature-profile/                  # optional multi-module feature
feature-game/                     # optional
```

Gradle:

```
settings.gradle.kts   # include modules
gradle/libs.versions.toml
```

Document actual layout in `project-context/MOBILE.md` after bootstrap.
