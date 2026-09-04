# Skill: Stack Selection

```
Name: stack-selection
Domain: architecture / bootstrap
Purpose: Choose language, framework, and tools from project type when the user does not specify a stack
Trigger: Greenfield project; "build a web/game/LLM app" without naming Django/React/etc.; empty or nearly empty repo; bootstrap finds no stack
Do Not Trigger: Existing codebase with clear stack — always match what is already there
```

## Non-negotiables

1. **Existing code wins.** If `manage.py`, `package.json`, Gradle, Unity, etc. exist → use that stack. Never “upgrade” the user’s stack unsolicited.
2. **User explicit choice wins.** If they say FastAPI, Flutter, Godot → use that.
3. **One coherent stack.** Don’t mix three backend frameworks or two state libraries.
4. **YAGNI.** Prefer the **default row** in `standards/DefaultStackMatrix.md` unless constraints force otherwise.
5. **Write the decision** into `project-context/STACK_DECISION.md` (and update `PROJECT_CONTEXT.md`) so future sessions don’t re-litigate.
6. **State assumptions** in the first reply: project type → chosen stack → why → how to override.

## Procedure

### 1. Classify project type

Infer from the user request (and ask **at most one** clarifying question only if type is ambiguous):

| Type | Signals |
|------|---------|
| **web-fullstack** | SaaS, dashboard, admin, CRUD site, “website with API” |
| **web-frontend** | Landing, marketing, static/marketing site only |
| **web-api** | API-only, BFF, microservice backend |
| **mobile-android** | Android app, Kotlin app, Play Store utility |
| **mobile-game** | Mobile game, casual game, Unity/Godot game |
| **desktop** | Desktop tool, Electron/Tauri |
| **data-pipeline** | ETL, batch jobs, analytics pipeline |
| **llm-app** | Chatbot, RAG, agents, AI product over docs/API |
| **cli-tool** | CLI, developer tool, scriptable utility |
| **library** | SDK, package, reusable library |

If still unclear: ask once — “Is this mainly a web app, mobile game, or LLM/RAG product?”

### 2. Apply defaults

Use `standards/DefaultStackMatrix.md`. Summarize:

- Languages
- Frameworks
- DB / cache / queue (if needed)
- Lint/test/build tools
- Docker yes/no
- Rigor skills/workflows to load next

### 3. Constraint overrides (only when present)

| Constraint | Prefer |
|------------|--------|
| User strongest in Python/Django | Django/DRF + React/Next (already matrix default for web) |
| Realtime multiplayer game | Engine + authoritative backend; not “React as game loop” |
| Heavy SEO content site | Next.js (or similar) SSR/SSG |
| Tiny internal API | FastAPI or Django — pick one; default FastAPI if “API only”, Django if “admin + ORM + users” |
| LLM + company already on Python | Python + FastAPI/Django + chosen LLM SDK |
| Must be offline mobile game | Unity/Godot; backend optional |

### 4. Record & proceed

1. Write `STACK_DECISION.md`.
2. Fill stack fields in `PROJECT_CONTEXT.md`.
3. Continue with `NewProjectBootstrap` or the matching feature workflow.
4. Do **not** ask the user to pick among five equivalent frameworks.

## Anti-patterns

- Asking “React or Vue or Svelte or Angular?” when default is fine
- Choosing microservices for an MVP
- Choosing Kubernetes for a Compose-sized app
- Replacing an existing working stack mid-project
- Picking a game engine for a CRUD admin panel

## Expected output

```markdown
## Stack decision
- Project type: web-fullstack
- Backend: Python, Django, DRF, PostgreSQL, Redis, Celery (as needed)
- Frontend: TypeScript, React or Next.js
- Tools: Ruff, pytest, ESLint/tsc, Docker Compose
- Rationale: …
- Override: say if you want FastAPI / Vue / etc.
```

## Related

`architecture`, `NewProjectBootstrap`, `DefaultStackMatrix`, domain skills after selection
