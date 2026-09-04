# Default Stack Matrix

Opinionated **defaults when the user does not specify** a stack.  
If the repo already has a stack, **ignore this matrix** and match the repo.

Rigor OS defaults lean toward stacks the primary user already uses well: **Python/Django**, **React/Next**, **PostgreSQL**, **Docker Compose**, **Android/Kotlin** or **Unity** for mobile games.

---

## web-fullstack

| Layer | Default | Tools |
|-------|---------|-------|
| Backend | Python 3.12+, **Django** + **DRF** | Ruff, pytest, mypy/pyright optional |
| DB | **PostgreSQL** | Django migrations |
| Cache / jobs | **Redis** + Celery when async needed | — |
| Frontend | **TypeScript** + **React** or **Next.js** (SEO/SSR → Next) | ESLint, tsc, Vitest/Jest as project grows |
| API contract | OpenAPI / DRF schema | openapi-typescript when FE+BE |
| Run | **Docker Compose** | multi-stage Dockerfiles |
| Profile | Medium | |

**Skills:** django-clean-architecture, api-engineer, frontend-ui-quality, contract-integrity, docker.

---

## web-api

| Layer | Default | Tools |
|-------|---------|-------|
| API | **Django+DRF** if admin/users/ORM-heavy; else **FastAPI** | Ruff, pytest |
| DB | PostgreSQL | Alembic if FastAPI |
| Docs | OpenAPI | Spectral optional |
| Run | Docker Compose | |

---

## web-frontend

| Layer | Default | Tools |
|-------|---------|-------|
| UI | **Next.js** + TypeScript (or Vite+React if pure SPA) | ESLint, tsc |
| Styling | Project design tokens / existing CSS approach | — |
| Host | Static/SSR as framework default | |

No backend invented unless the request needs one.

---

## mobile-android

| Layer | Default | Tools |
|-------|---------|-------|
| App | **Kotlin** + **Jetpack Compose** | Gradle, Android Lint, unit tests |
| Architecture | MVVM / existing Clean layout | Hilt/Koin as siblings |
| Backend (if needed) | Django+DRF or existing API | contract-integrity |
| Run | Emulator + Compose assembleDebug | |

**Skills:** android-app, mobile-api-client, mobile-ui-ux, MobileGate.

---

## mobile-game

| Layer | Default | Tools |
|-------|---------|-------|
| Client | **Unity** (2D/3D general) or **Godot** (lighter/2D/open) — prefer Unity if 3D/asset store; Godot if small 2D and user wants open stack | Android export |
| Backend | **Django+DRF** + PostgreSQL for accounts, leaderboards, IAP verify | Redis if needed |
| Authority | Server for score/currency/IAP | mobile-backend-api |
| Run | Device/emulator smoke + Compose/Unity Android build | |

**Skills:** mobile-game, mobile-backend-api, engine overlay.

---

## llm-app

| Layer | Default | Tools |
|-------|---------|-------|
| API | **Python** + **FastAPI** (or Django if same monorepo as main product) | Ruff, pytest |
| Orchestration | Simple service layer first; LangGraph/equivalent only if multi-agent needed | — |
| Retrieval | pgvector on PostgreSQL or managed vector store if already in org | — |
| LLM | Provider via env keys (OpenAI/Anthropic/etc.) — never commit keys | — |
| Frontend | Next.js/React chat UI if user-facing | |
| Eval | Fixture prompts + basic regression checks | |
| Run | Docker Compose | |

**Do not** start with a multi-agent mesh. YAGNI.

**Skills:** backend-quality, api-engineer, observability, security (secrets), frontend if UI.

---

## data-pipeline

| Layer | Default | Tools |
|-------|---------|-------|
| Language | **Python** | Ruff, pytest |
| Schedule | Celery / cron / existing worker | Redis |
| Storage | PostgreSQL + object storage if files | |
| Run | Docker | |

---

## cli-tool

| Layer | Default | Tools |
|-------|---------|-------|
| Language | **Python** (Typer/Click) or **Go** if single static binary required | pytest / go test |
| Packing | pipx / uv or Go release | |

---

## desktop

| Layer | Default | Tools |
|-------|---------|-------|
| Shell | **Tauri** + web UI or **Electron** if team already on Electron | — |
| Prefer | Tauri for smaller footprint when greenfield | |

---

## library / SDK

| Layer | Default | Tools |
|-------|---------|-------|
| Match consumers | Python package if Python clients; TypeScript if npm | pytest / vitest |
| Versioning | SemVer | |

---

## Decision shortcuts

```
Has existing repo stack? → use it
Else user named a stack? → use it
Else classify type → this matrix default
Else ask ONE question (web vs mobile game vs LLM)
```

## Anti-defaults (avoid unless required)

- Microservices for MVP
- Kubernetes for single Compose app
- Mongo “because JSON” when PostgreSQL fits
- Flutter for Android-only when Kotlin Compose is enough and backend is Django-centric
- New frontend meta-framework every project
