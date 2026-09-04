# New Project Bootstrap Workflow

Initialize a new repository with this OS and project-specific context.

## Flow

```
Detect or ask: project type, stack, architecture
    → Copy rigor-os into repo
    → Run tools/bootstrap.py (Django, Node, Android/Gradle, Unity, Godot)
    → Fill PROJECT_CONTEXT, COMMANDS, ARCHITECTURE, MOBILE (if mobile)
    → Install adapter (Cursor first)
    → Optional: copy docker templates
    → Verify agent can run lint/test/assemble commands
```

## Detect

The bootstrap script looks for:

- `manage.py`, `pyproject.toml`, `requirements.txt` → Python/Django
- `package.json` → Node/React/Next
- `build.gradle*` / `AndroidManifest.xml` → Android
- Unity `ProjectSettings` / Godot `project.godot` → game engines
- `Dockerfile`, `compose.yml` → containers
- CI configs (GitHub Actions, GitLab CI)
- Test runners (pytest, vitest, jest, Gradle test)

Ask the user only for what cannot be inferred (deployment target, profile size, store listing).

## Outputs

- `project-context/PROJECT_CONTEXT.md`
- `project-context/COMMANDS.md`
- `project-context/ARCHITECTURE.md`
- `project-context/MOBILE.md` (when mobile detected)
- Adapter files in `.cursor/` (or CLAUDE.md / AGENTS.md)

## Docker

If user wants easy bring-up, copy `docker/fullstack/` and adjust service names. Goal: `docker compose up` works with documented `.env`. For mobile, point the Android emulator at the host API (`10.0.2.2` for Android emulator → host localhost).
