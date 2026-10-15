# Model & Token Routing Matrix

Rigor OS routes **task complexity** → **model tier** and **context load**.  
Low tasks must not burn flagship models. Leads (orchestrator planning, security/architecture review) use the **highest** tier available in the project.

Concrete model IDs live in `project-context/MODEL_ROUTING.md` (per project / per tool).

---

## Model tiers (logical)

| Tier | Role | Use for |
|------|------|---------|
| **T0 — Economy** | Fast / cheap | Typos, renames, one-line fixes, comment-only, simple CSS/token tweak, regenerate types after known schema |
| **T1 — Standard** | Default implementer | Single-domain bug/feature, one module, clear sibling pattern |
| **T2 — Strong** | Hard implementer | Multi-file feature, API+client, migrations, flaky diagnosis, non-trivial UI |
| **T3 — Max** | Lead / governor | Orchestrator planning for Medium+ work, Security Reviewer, Architecture Reviewer, ambiguous root-cause, cross-domain design, incident triage |

If only one model is available, use it for everything but still **reduce context** (skills/gates) for T0/T1.

---

## Role → minimum tier

| Role | Min tier | Notes |
|------|----------|-------|
| Orchestrator — classify + route only | T1 | Cheap classify OK |
| Orchestrator — plan Medium/Large feature + DoD | **T3** | Highest available |
| Implementer T0/T1 work | T0 / T1 | Do not escalate without failure |
| Implementer T2 work | T2 | Escalate to T3 after 2 failed verify loops |
| Security Reviewer | **T3** | Always highest; read-only |
| Architecture Reviewer | **T3** | Always highest; read-only |
| Stack selection (greenfield) | T2 | Defaults are in matrix; T3 if constraints weird |

---

## Task → tier (classify first)

| Signals | Tier |
|---------|------|
| Typo, lint autofix, rename symbol, copy change, color/spacing | **T0** |
| One service method, one endpoint sibling, one Compose screen following sibling | **T1** |
| Feature across layers, OpenAPI+FE/mobile, migration, auth touch, game economy client | **T2** |
| New architecture, security-sensitive design, multi-domain product slice, production incident | **T3** (+ reviewers as needed) |

When unsure between two tiers, pick the **lower** first; escalate if blocked.

---

## What NOT to spawn (token waste)

| Task tier | Forbidden |
|-----------|-----------|
| T0 | Security Reviewer, Architecture Reviewer, >1 skill body, E2E, ADR |
| T1 | Architecture Reviewer; Security Reviewer unless auth/PII touched |
| T2 | Architecture Reviewer unless new module/boundary; max 3 skills |
| T3 | Still max 3 skills at once; prefer tools over loading encyclopedias |

---

## Context budget by tier

| Tier | Max skills loaded | Gates | Review agents |
|------|-------------------|-------|---------------|
| T0 | 0–1 | Lint only | None |
| T1 | 1–2 | Lint + relevant unit tests | None (unless auth) |
| T2 | ≤3 | Per QualityGateMatrix | Security if auth/economy |
| T3 | ≤3 + targeted refs | Full applicable matrix | Security and/or Architecture as justified |

Progressive disclosure still applies: L1 constitution always; skill **bodies** only when needed.

---

## Escalation policy

```
Start at classified tier
    → fail verify ×2 → bump one tier (T0→T1→T2→T3)
    → fail ×3 at T3 → BLOCKED (human)
Never start a CSS fix at T3.
Never run Architecture Reviewer on a typo.
```

---

## Tool mapping (adapters)

| Logical tier | Cursor | Claude Code | Codex / Copilot |
|--------------|--------|-------------|-----------------|
| T0–T1 | Faster/cheaper model if UI allows; avoid Task subagents | `haiku` / `sonnet`, effort `low`–`medium` | Default smaller / fewer turns, low reasoning |
| T2 | Default strong agent model | `sonnet`, effort `high` | Default agent, medium–high reasoning |
| T3 | Best available / thinking model; reviewers as subagents with best model | `opus` (or strongest available), effort `xhigh`/`max`; subagent `model:` + `effort:` frontmatter | Best available, high reasoning |

## Reasoning effort is the second dial

Many tools now expose a reasoning-effort setting next to the model (Claude Code `effort: low|medium|high|xhigh|max`
in subagent frontmatter and the session; Codex `model_reasoning_effort`). Route both:

| Tier | Model alias | Effort |
|------|-------------|--------|
| T0 | economy | low |
| T1 | standard | medium |
| T2 | strong | high |
| T3 | max | xhigh / max |

Cheaper than switching models: drop effort first for routine T1 work; raise effort before escalating the model.

## Prompt caching

Keep the always-loaded kernel (CLAUDE.md / AGENTS.md / constitution) stable and at the top of context — edits to
it invalidate cached prefixes for every session. Put volatile notes in `project-context/` files that are read on demand.

Exact IDs: `project-context/MODEL_ROUTING.md`.
