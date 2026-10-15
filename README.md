# Rigor OS

**An engineering operating system for AI coding agents.**

Drop this into a repository. Then say *“build this feature.”*  
The agent should plan, implement, integrate, verify, and only call the work done when there is **evidence** — not vibes.

Works with **Cursor** (first-class), plus adapters for **Claude Code**, **OpenAI Codex**, and **GitHub Copilot**.

> **This is an optimized fork** of [sajadfallahdoost/rigor-os](https://github.com/sajadfallahdoost/rigor-os), refreshed for October 2026.
> It keeps the original architecture and adds an SEO agent, MCP governance, PostgreSQL scaling (with
> [shahrah](https://github.com/mahdi-noori-ai/shahrah)), hardened CI/CD and Docker templates, one tested safety
> hook for every tool, and its own test suite. See [CHANGELOG](CHANGELOG.md) for every change and why.

---

## What's new in this fork

| Area | Change |
|------|--------|
| **SEO agent** | `seo-strategist` agent + `seo-context` skill + `SEOGate`. `tools/seo_context.py` extracts routes, metadata, headings, JSON-LD, OG, crawl files, and seed terms from Next.js / Astro / SvelteKit / Nuxt / Remix / HTML / Django / Markdown, then the agent writes per-route specs and a plan for Google, Bing, AI answer engines, rich results, social, app stores, and GitHub/registries |
| **Safety hooks** | One stdlib hook (`adapters/hooks/guard_shell.py`, 45 tests) for Claude Code, Codex, and Cursor. Fixes the Codex `hooks.json` shape, the Cursor hook that allowed everything when `jq` was missing, and the deprecated Claude output format; adds force-push, `curl \| sh`, `.env` printing, volume-wipe, and infra-teardown rules |
| **Agent Skills** | Skills moved to `adapters/skills/` in the open [Agent Skills](https://agentskills.io) format and installed for every tool (`.claude/skills`, `.agents/skills` for Codex, `.github/skills` for Copilot, `.cursor/skills`). Claude Code went from 1 skill to 18 |
| **Subagents** | Reviewers pinned read-only (`disallowedTools`, `permissionMode: plan`) on `opus` with `effort`; Copilot custom agents added |
| **MCP** | `mcp-governance` skill for MCP spec 2026-07-28 (stateless core, OAuth `iss` validation, CIMD) and the OWASP Agentic Top 10; pinned `.mcp.json` template; bootstrap inventories MCP servers |
| **Database** | `postgres-scaling` skill (measure → index → pool → replicas → partition → shard), `pg_stat_statements` on by default, PgBouncer profile, shahrah overlay for multi-region data residency |
| **CI/CD** | SHA-pinned GitHub Actions template with `permissions: {}`, zizmor, gitleaks, dependency review, SBOM + provenance attestations; Dependabot; this repo now has its own CI |
| **Docker** | Postgres 18 (fixes the new volume path), Python 3.14 + uv, Node 24, Redis 8 / Valkey, unprivileged nginx, cache mounts, required secrets, fixed broken build-context paths |
| **Security** | OWASP Top 10:2025 + Agentic Top 10 in `SecurityGate`; Constitution Principle 9 (untrusted input is data) |
| **Tools** | `bootstrap.py` no longer overwrites your edited context, prunes `node_modules`, detects uv/pnpm/Next/FastAPI/Rust/Go/MCP/SEO surfaces; `validate-gates.sh` no longer turns failures into passes; `sync-adapters.sh` works in both layouts and backs up files it replaces |
| **Model routing** | Reasoning *effort* as the second routing dial; prompt-cache-friendly kernel guidance |
| **Claude Code plugin** | `/plugin marketplace add mahdi-noori-ai/rigor-os` — skills, agents, guard hook, and a SessionStart kernel without copying files |

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
git clone https://github.com/mahdi-noori-ai/rigor-os.git /path/to/your-project/rigor-os

# 2. Detect stack and fill project memory
cd /path/to/your-project
python3 rigor-os/tools/bootstrap.py          # re-runnable; keeps files you edited

# 3. Install an adapter (or `all`)
bash rigor-os/tools/sync-adapters.sh cursor   # claude | codex | copilot | all

# 4. Run the gates any time
bash rigor-os/tools/validate-gates.sh
```

Then in the agent:

> Build user profile management with backend API, frontend forms, auth, validation, and database changes.

It should inspect siblings, pick skills, implement in a sensible order, verify integration, and attach **command output** — or report **BLOCKED** instead of fake success.

### Install as a Claude Code plugin

No vendoring needed — the repository is also a plugin marketplace:

```text
/plugin marketplace add mahdi-noori-ai/rigor-os
/plugin install rigor-os@rigor-os
```

You get the 18 skills (namespaced `rigor-os:<skill>`), the `security-reviewer`, `architecture-reviewer`, and
`seo-strategist` agents, the destructive-command guard (`PreToolUse`), and a `SessionStart` hook that loads the
constitution kernel and tells Claude where the plugin lives. Project context still lives in your repo: run
`python3 <plugin path>/tools/bootstrap.py --root .` once (the session kernel prints the exact command).
Plugins cannot set permission rules, so copy the `deny` list from
[`adapters/claude/settings.json`](adapters/claude/settings.json) into `.claude/settings.json` if you want
`.env` reads blocked too.

Other tools:

```bash
bash rigor-os/tools/sync-adapters.sh claude
bash rigor-os/tools/sync-adapters.sh codex
bash rigor-os/tools/sync-adapters.sh copilot
```

If you vendor the contents at the **repo root** (this repository’s layout), use `./tools/...`; the scripts detect both layouts.

---

## Easy Docker bring-up

Templates live in [`docker/`](docker/) (Django + React + Postgres + Redis + Nginx).

```bash
cp rigor-os/docker/fullstack/.env.example .env      # set SECRET_KEY
docker compose -f rigor-os/docker/fullstack/compose.yml --env-file .env up --build
# + PgBouncer:  --profile pooler   (and DB_HOST=pgbouncer)
```

Images are **multi-stage**, run as **non-root**, use **BuildKit cache mounts**, and include **healthchecks**. Postgres 18, Redis 8 (or Valkey), Python 3.14 + uv, Node 24, unprivileged nginx. Multi-region data: [`docker/shahrah/`](docker/shahrah/compose.yml).

---

## What’s inside

```
rigor-os/
├── constitution/      # L1 kernel (~800 tokens)
├── agents/            # Orchestrator + review specs
├── skills/            # Backend, frontend/UI, mobile/Android/game, API, DB, security, Docker…
├── workflows/         # Feature, bug, API change, migration, hotfix…
├── quality-gates/     # DoD, testing, security, architecture, contracts
├── adapters/          # Cursor, Claude, Codex, Copilot + shared skills/ and hooks/
├── docker/            # Compose stacks: fullstack, django, react, shahrah
├── templates/         # ADR, specs, CI (templates/ci), mcp.json, SEO context, llms.txt
├── tools/             # bootstrap.py, sync-adapters.sh, validate-gates.sh, seo_context.py, check_links.py
├── tests/             # pytest suite for the tools and hooks
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

## Automatic stack selection

If you say *“build a web app”* or *“build a mobile game”* **without** naming Django/React/Unity/etc., and the repo has no stack yet, Rigor OS:

1. Classifies project type (web, Android, game, LLM, …)
2. Applies opinionated defaults from [`standards/DefaultStackMatrix.md`](standards/DefaultStackMatrix.md) (Django+DRF, React/Next, PostgreSQL, Compose, Kotlin/Unity, Python for LLM, …)
3. Writes [`project-context/STACK_DECISION.md`](project-context/STACK_DECISION.md)
4. Continues bootstrap / implementation

**Existing code always wins.** Explicit user stack always wins. You can override in one sentence.

Skill: [`stack-selection`](skills/architecture/StackSelectionSkill.md) · Workflow: [`StackSelection`](workflows/StackSelection.md)

---

## SEO agent

Anything you publish gets an SEO context generated from its **layouts and pages**:

```bash
python3 rigor-os/tools/seo_context.py --base-url https://example.com   # → project-context/SEO_CONTEXT.{md,json}
python3 rigor-os/tools/seo_context.py --check                          # CI gate: indexable pages need title + description
```

The extractor is deterministic (no network): routes (incl. Next.js route groups and dynamic segments), titles and
templates, descriptions, H1/H2, canonical, robots, `lang`, hreflang, Open Graph/Twitter, JSON-LD types, images
missing `alt`, internal links, seed terms from visible copy, plus `robots.txt` / sitemap / `llms.txt` / manifest /
README / `package.json` / `pyproject.toml` / `AndroidManifest.xml` signals.

The **SEO Strategist** agent ([spec](agents/seo-strategist/SEOStrategistSpec.md)) then writes positioning,
intent and keyword clusters, an entity map, per-route title/description/H1/canonical/OG/JSON-LD specs, crawl files,
and a channel plan for **Google, Bing (+IndexNow), AI answer engines (AI Overviews/AI Mode, ChatGPT search,
Perplexity, Claude), rich results, social cards, image/video, Play Store ASO, and GitHub/package registries** —
appended under `<!-- agent-notes -->` so reruns keep it. Gate: [SEOGate](quality-gates/SEOGate.md).

---

## Token & model management

Rigor OS decides **how heavy** each task should be:

| Tier | Examples | Model | Reviewers |
|------|----------|-------|-----------|
| **T0** | Typo, rename, tiny CSS | Economy | None |
| **T1** | Single-module bug/feature | Standard | Rarely |
| **T2** | API + client, migrations | Strong | Security if auth |
| **T3** | Architecture, incidents, hard design | **Max** | Security/Arch @ **max** |

Per-project model IDs: [`project-context/MODEL_ROUTING.md`](project-context/MODEL_ROUTING.md).  
Policy: [`standards/ModelRoutingMatrix.md`](standards/ModelRoutingMatrix.md) · Skill: [`token-model-routing`](skills/architecture/TokenModelRoutingSkill.md).

Orchestrator/planning and review **leads** use the highest tier; low tasks must not.

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
| [Default stack matrix](standards/DefaultStackMatrix.md) | Languages/frameworks when you don’t specify |
| [Model routing matrix](standards/ModelRoutingMatrix.md) | T0–T3 models & who uses max |
| [Failure scenarios](examples/FailureScenarios.md) | How vibe-coding failures get caught |
| [SEO context skill](skills/seo/SEOContextSkill.md) · [SEO gate](quality-gates/SEOGate.md) | Search surfaces, metadata, structured data |
| [MCP governance](skills/ai/MCPGovernanceSkill.md) | Adding/building MCP servers safely |
| [PostgreSQL scaling](skills/database/PostgresScalingSkill.md) | Indexes → pooling → replicas → sharding (shahrah) |
| [CI/CD](skills/devops/CICDSkill.md) · [CI template](templates/ci/github-actions-ci.yml) | Hardened GitHub Actions |
| [Changelog](CHANGELOG.md) | What this fork changed and why |

---

## Developing Rigor OS

```bash
uv run --with pytest python -m pytest -q   # tools + hooks
uvx ruff check . && uvx ruff format --check .
python3 tools/check_links.py               # no orphaned references
```

CI runs the same commands plus shellcheck, compose validation, an adapter-sync smoke test, and zizmor.

## Credits & license

Original framework by [Sajad Fallahdoost](https://github.com/sajadfallahdoost/rigor-os); shahrah by
[rs-alireza](https://github.com/rs-alireza/shahrah) (MIT). The upstream repository has no explicit license file;
its README says "Use and adapt in your projects", and this fork follows that. Improve the OS itself via
[Framework Evolution](evolution/FrameworkEvolution.md).
