# New Project Bootstrap Workflow

Initialize a new repository with this OS and project-specific context.

## Flow

```
Detect existing stack OR run Stack Selection (if none / user silent)
    → Copy rigor-os into repo (if not already)
    → Run tools/bootstrap.py (Django, Node, Android/Gradle, Unity, Godot)
    → Fill PROJECT_CONTEXT, COMMANDS, ARCHITECTURE, MOBILE, STACK_DECISION
    → Install adapter (Cursor first)
    → Optional: copy docker templates for chosen stack
    → Verify agent can run lint/test/assemble commands
```

## Stack when user is silent

If the repo is empty / undetectable and the user did not name Django, React, Unity, etc.:

1. Run workflow `StackSelection.md` + skill `stack-selection`.
2. Apply `standards/DefaultStackMatrix.md` by project type (web, mobile game, LLM, …).
3. Write `project-context/STACK_DECISION.md`.
4. Tell the user the choice and that they can override in one sentence.

**Never** re-pick a stack when bootstrap already found one.

## Detect

The bootstrap script looks for:

- `manage.py`, `pyproject.toml`, `requirements.txt` → Python/Django
- `package.json` → Node/React/Next
- `build.gradle*` / `AndroidManifest.xml` → Android
- Unity `ProjectSettings` / Godot `project.godot` → game engines
- `Dockerfile`, `compose.yml` → containers
- CI configs (GitHub Actions, GitLab CI)
- Test runners (pytest, vitest, jest, Gradle test)

Ask the user only for what cannot be inferred (deployment target, profile size, store listing) — **not** a long framework menu.

## Outputs

- `project-context/PROJECT_CONTEXT.md`
- `project-context/COMMANDS.md`
- `project-context/ARCHITECTURE.md`
- `project-context/MOBILE.md` (when mobile detected)
- `project-context/STACK_DECISION.md` (when stack was chosen or N/A)
- Adapter files in `.cursor/` (or CLAUDE.md / AGENTS.md)

## Docker

If user wants easy bring-up, copy `docker/fullstack/` and adjust service names. Goal: `docker compose up` works with documented `.env`. For mobile, point the Android emulator at the host API (`10.0.2.2` for Android emulator → host localhost).
