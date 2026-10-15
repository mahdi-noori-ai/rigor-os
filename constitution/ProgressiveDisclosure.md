# Progressive Disclosure Model

Context efficiency strategy for AI coding agents. Minimize always-loaded tokens; maximize relevant depth on demand.

## Four Levels

### Level 1 — Constitution (Always Loaded)

**What:** Root principles, project profile, safety rules.
**Files:** `constitution/CONSTITUTION.md`, `project-context/PROJECT_CONTEXT.md` (summary).
**Token budget:** ~800 tokens total.
**Loaded when:** Every interaction.

### Level 2 — Domain Awareness (Always Loaded, Lightweight)

**What:** Skill and workflow names + one-line descriptions only.
**Files:** Skill frontmatter `description` fields; workflow index.
**Token budget:** ~50 tokens per skill (descriptions only, not bodies).
**Loaded when:** Every interaction (agent knows what exists).

### Level 3 — Active Skill (On Demand)

**What:** Full skill body with procedures, checks, anti-patterns.
**Files:** `skills/**/**Skill.md`, `workflows/*.md`.
**Token budget:** ~500–2000 tokens per skill.
**Loaded when:** Task matches skill `description` or workflow is explicitly invoked.

### Level 4 — References and Templates (Explicit Request)

**What:** Detailed examples, ADR templates, migration plans, API contract samples.
**Files:** `templates/*`, `skills/*/references/*`, OpenAPI specs.
**Token budget:** Variable.
**Loaded when:** Active skill explicitly references them.

## Loading Rules

1. Never load all skills at once.
2. Load at most 3 skills simultaneously for a task.
3. Unload skill context when switching to a different domain.
4. Prefer deterministic tools over loading a skill for verification.

## Model tier coupling

Combine with `standards/ModelRoutingMatrix.md`:

| Task tier | Context | Model alias |
|-----------|---------|-------------|
| T0 | L1 only (+ tiny edit) | economy |
| T1 | L1 + 1–2 skills | standard |
| T2 | L1 + ≤3 skills + gates | strong |
| T3 plan/review | L1 + targeted skills + reviewers | **max** |

Do not load L4 references on T0/T1.

## Tool-Specific Mapping

### Cursor

| Level | Mechanism |
|-------|-----------|
| L1 | `AGENTS.md` + `rules/constitution.mdc` (`alwaysApply: true`) |
| L2 | `.cursor/skills/*/SKILL.md` (also reads `.agents/skills`, `.claude/skills`) description in frontmatter |
| L3 | Full `SKILL.md` body loaded when agent matches description |
| L4 | `references/` subdirectory within skill folder |

Path-scoped rules (`globs`) load additional L1 constraints for specific file types without loading globally.

### Claude Code

| Level | Mechanism |
|-------|-----------|
| L1 | `CLAUDE.md` |
| L2 | Skill `description` in frontmatter (auto-invocation) |
| L3 | Full `SKILL.md` when Claude decides it's relevant |
| L4 | `references/` in skill folder |

### OpenAI Codex

| Level | Mechanism |
|-------|-----------|
| L1 | `AGENTS.md` (32 KiB budget — keep root lean) |
| L2 | Nested `AGENTS.md` in subdirectories (closer = higher precedence) |
| L3 | Agent Skills in `.agents/skills/*/SKILL.md` (cwd → repo root) |
| L4 | Referenced files loaded on demand |

**Warning:** Codex truncates combined AGENTS.md chain at `project_doc_max_bytes` (default 32 KiB). Root-first loading means large root files starve nested instructions. Keep root AGENTS.md under 8 KiB.

### GitHub Copilot

| Level | Mechanism |
|-------|-----------|
| L1 | `AGENTS.md` + `.github/copilot-instructions.md` |
| L2 | Agent Skills in `.github/skills` (also `.agents/skills`, `.claude/skills`) |
| L3 | `.github/instructions/*.instructions.md` (path-scoped via `applyTo`) |
| L4 | Referenced docs |

## Anti-Patterns

- One giant system prompt with everything
- `alwaysApply: true` on procedural skills (use description-triggered instead)
- Duplicating the same instruction in rules AND skills AND agents
- Loading architecture docs when fixing a CSS bug
- Creating a new agent when a skill suffices

## Decision: Rule vs Skill vs Agent

```
Is it a non-negotiable constraint for every turn?
  YES → Rule (alwaysApply or globs)
  NO ↓
Is it a multi-step procedure for a specific task type?
  YES → Skill (description-triggered)
  NO ↓
Does it need independent context from the implementer?
  YES → Agent (security/architecture review only)
  NO → Workflow document referenced by orchestrator
```
