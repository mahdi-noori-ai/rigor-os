# New Project Bootstrap Workflow

Initialize a new repository with this OS and project-specific context.

## Flow

```
Detect or ask: project type, stack, architecture
    → Copy rigor-os into repo
    → Run tools/bootstrap.py
    → Fill PROJECT_CONTEXT, COMMANDS, ARCHITECTURE
    → Install adapter (Cursor first)
    → Optional: copy docker templates
    → Verify agent can run lint/test commands
```

## Detect

The bootstrap script looks for:

- `manage.py`, `pyproject.toml`, `requirements.txt` → Python/Django
- `package.json` → Node/React/Next
- `Dockerfile`, `compose.yml` → containers
- CI configs (GitHub Actions, GitLab CI)
- Test runners (pytest, vitest, jest)

Ask the user only for what cannot be inferred (deployment target, profile size).

## Outputs

- `project-context/PROJECT_CONTEXT.md`
- `project-context/COMMANDS.md`
- `project-context/ARCHITECTURE.md`
- Adapter files in `.cursor/` (or CLAUDE.md / AGENTS.md)

## Docker

If user wants easy bring-up, copy `docker/fullstack/` and adjust service names. Goal: `docker compose up` works with documented `.env`.
