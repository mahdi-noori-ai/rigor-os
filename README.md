# Rigor OS

**An engineering operating system for AI coding agents.**

Drop this into a repository. Then say *“build this feature.”*  
The agent should plan, implement, integrate, verify, and only call the work done when there is **evidence** — not vibes.

Works with **Cursor** (first-class), plus adapters for **Claude Code**, **OpenAI Codex**, and **GitHub Copilot**.

---

## The problem

AI agents are fast. On real products they still:

- forget architecture and invent a parallel style
- change an API and leave the frontend behind
- skip tests, or comment them out to go green
- ship desktop-only UI that looks like a default template
- miss authorization, unsafe migrations, and N+1 queries
- declare success because “there were no obvious errors”

Rigor OS is the missing **engineering organization** around a single implementer: constitution, skills, workflows, quality gates, and tool adapters — without a swarm of fake specialist agents.

---

## What it is

```
Hybrid orchestrator + on-demand skills + deterministic gates
```

| Layer | Role |
|--------|------|
| **Constitution** | Always-on: match existing code, smallest diff, no false success |
| **Skills** | Load only when relevant (API, Django, UI, Android/mobile game, Docker, security…) |
| **Workflows** | Feature, bug, refactor, API change, migration, mobile/game, incident, release |
| **Quality gates** | Lint/tests/contract/security/architecture/**mobile** — contextual, not theater |
| **Adapters** | Same canonical docs → Cursor / Claude / Codex / Copilot |
| **Docker starters** | Multi-stage, non-root, healthchecks — `compose up` as the easy path |

**Three agent roles only:** the main session (orchestrator), plus optional **read-only** Security and Architecture reviewers. No agent explosion.

**Completion rule:** writing code is not done.

```
Requirement → Architecture → Implementation → Integration → Verification → User behavior
```

---

## Quick start

```bash
# 1. Clone into your product repo (or copy this folder)
git clone https://github.com/sajadfallahdoost/rigor-os.git
cp -r rigor-os /path/to/your-project/

# 2. Detect stack and fill project memory
cd /path/to/your-project
python rigor-os/tools/bootstrap.py

# 3. Install Cursor adapter (recommended)
bash rigor-os/tools/sync-adapters.sh cursor
```

Then in the agent:

> Build user profile management with backend API, frontend forms, auth, validation, and database changes.

It should inspect siblings, pick skills, implement in a sensible order, verify integration, and attach **command output** — or report **BLOCKED** instead of fake success.

Other tools:

```bash
bash rigor-os/tools/sync-adapters.sh claude
bash rigor-os/tools/sync-adapters.sh codex
bash rigor-os/tools/sync-adapters.sh copilot
```

If you vendor the contents at the **repo root** (this repository’s layout), use `./tools/...` and paths without the `rigor-os/` prefix.

---

## Easy Docker bring-up

Templates live in [`docker/`](docker/) (Django + React + Postgres + Redis + Nginx).

```bash
cp docker/fullstack/.env.example .env
# Point compose build contexts at your app, then:
docker compose -f docker/fullstack/compose.yml up --build
```

Images are **multi-stage**, run as **non-root**, and include **healthchecks**. Adjust `Dockerfile` `CMD` / `collectstatic` to your project layout.

---

## What’s inside

```
rigor-os/
├── constitution/      # L1 kernel (~800 tokens)
├── agents/            # Orchestrator + review specs
├── skills/            # Backend, frontend/UI, mobile/Android/game, API, DB, security, Docker…
├── workflows/         # Feature, bug, API change, migration, hotfix…
├── quality-gates/     # DoD, testing, security, architecture, contracts
├── adapters/          # Cursor, Claude, Codex, Copilot
├── docker/            # Easy local/prod-shaped Compose
├── tools/             # bootstrap.py, sync-adapters.sh
└── research/          # Why this architecture (cited)
```

Technology-agnostic **core**, with a **Django clean-architecture overlay**, **UI design** skills, and a full **Android / mobile game** domain (client structure, server-authoritative game APIs, release).

---

## Mobile & Android games

Rigor OS also covers **Android apps** and **mobile games** that talk to your backend:

| Area | What you get |
|------|----------------|
| Client | `skills/mobile/` — Android structure, Compose/Kotlin overlay, UI/UX, testing, security, Play release |
| Game | Server-authoritative score/currency/IAP, HUD vs sim separation, Unity/Godot overlays |
| Backend | `mobile-backend-api` — mobile-friendly contracts, idempotent rewards, push tokens, force-update |
| Workflows | `MobileFeature`, `MobileGameFeature`, `AndroidRelease` |
| Gates | `MobileGate` + extended DoD / matrix columns |

Example walkthrough: [Mobile game leaderboard](examples/MobileGameLeaderboardFeature.md).

Fill [`project-context/MOBILE.md`](project-context/MOBILE.md) after bootstrap when Gradle/Unity/Godot is detected.

---

## Design principles

1. Match the existing codebase before inventing a style  
2. Prefer **tools** over prompts (Ruff > “please format”)  
3. Progressive disclosure — don’t dump the handbook every turn  
4. API contract integrity for frontend + backend  
5. Contextual Definition of Done (a CSS tweak is not a security review)  
6. Max 3 verify/fix loops, then **BLOCKED** with evidence  

Read the [research report](research/ResearchReport.md) for Cursor/Claude/Codex/Copilot mappings and why a deep agent hierarchy was rejected.

---

## Project size profiles

| Profile | When | Active gates |
|---------|------|-------------|
| **Small** | MVP, single service | Lint, unit tests, basic DoD |
| **Medium** | Production app, multiple domains | + integration tests, security, API contract |
| **Large** | Complex product, multiple services | + E2E, performance, observability, arch review |

Set the profile in [`project-context/PROJECT_CONTEXT.md`](project-context/PROJECT_CONTEXT.md) after bootstrap.

---

## Docs

| Doc | Why |
|-----|-----|
| [Constitution](constitution/CONSTITUTION.md) | Always-on rules |
| [Orchestrator](agents/orchestrator/OrchestratorSpec.md) | How the main agent should work |
| [Definition of Done](quality-gates/DefinitionOfDone.md) | When work is actually finished |
| [Quality gate matrix](quality-gates/QualityGateMatrix.md) | Which gates apply to which change |
| [Cursor adapter](adapters/cursor/ADAPTER_GUIDE.md) | `.cursor/rules`, skills, hooks |
| [Example: user profile](examples/UserProfileFeature.md) | End-to-end walkthrough |
| [Example: mobile game + API](examples/MobileGameLeaderboardFeature.md) | Android/game + Django rewards/leaderboard |
| [Mobile gate](quality-gates/MobileGate.md) | Android/game completion checks |
| [Failure scenarios](examples/FailureScenarios.md) | How vibe-coding failures get caught |

---

## License

Use and adapt in your projects. Improve the OS itself via [Framework Evolution](evolution/FrameworkEvolution.md).
