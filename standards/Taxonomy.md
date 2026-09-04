# Taxonomy: Rules, Skills, Agents, Workflows, Templates, Tools

## Rules

Persistent constraints. Short. Enforced every relevant turn.

**Belong here:** never commit secrets; match existing structure; no unrelated diffs; do not skip tests; follow sibling API shapes.

**Do not belong:** multi-page procedures; framework tutorials; full OWASP essays.

**Cursor:** `.mdc` with `alwaysApply` or `globs`.
**Claude:** `CLAUDE.md` bullets.
**Codex:** lean `AGENTS.md`.

## Skills

Reusable procedures loaded when the task matches a precise `description`.

**Belong here:** how to review a migration; how to design REST errors; how to make a non-robotic UI; Django layering overlay.

**Structure (canonical):** Non-negotiables → responsibilities table → workflow steps → anti-patterns → checks.

## Agents

Independent context with different incentives or tool sets.

**Justified agents (only three):**

1. Orchestrator — the main session (governance), not a spawn.
2. Security Reviewer — adversarial, read-only.
3. Architecture Reviewer — global structure, read-only.

**Not agents:** "Pagination specialist", "Redis specialist", "Unit test engineer" — those are skills.

## Workflows / Playbooks

Multi-step processes that sequence skills and gates.

**Belong here:** feature implementation, bug fix, API change, incident.

## Templates

Reusable artifacts: ADR, feature spec, OpenAPI stub, test plan.

## Deterministic tools (prefer over LLM)

| Instead of | Use |
|------------|-----|
| "Don't make syntax errors" | Compiler |
| "Follow style" | Ruff / Prettier / ESLint |
| "Don't break types" | mypy / tsc |
| "Don't drift API" | OpenAPI + oasdiff + contract tests |
| "Don't ship secrets" | Hook / gitleaks |
| "Don't break behavior" | pytest / vitest |

## File Responsibility Matrix (core)

| Path | Purpose | Loaded when | Owner | Modifies code? |
|------|---------|-------------|-------|----------------|
| `constitution/CONSTITUTION.md` | L1 kernel | Always | Human | No |
| `constitution/SafeAutonomy.md` | Safety | Always via adapter rules | Human | No |
| `agents/orchestrator/OrchestratorSpec.md` | How the main agent works | Feature/complex tasks | Human | Yes (via agent) |
| `agents/security-reviewer/*` | Independent AppSec | Security-sensitive | Human | No |
| `agents/architecture-reviewer/*` | Independent arch | Large changes | Human | No |
| `skills/mobile/**` | Android app & game procedures | Mobile/Android/game tasks | Human | Via implementer |
| `skills/**` | Domain procedures | Task match | Human | Via implementer |
| `workflows/**` | Playbooks | Task type | Human | Via implementer |
| `quality-gates/**` | Verification | Before DONE | Human | No |
| `project-context/**` | Project memory | Always (summary) | Bootstrap + human | No |
| `adapters/**` | Tool mapping | Install time | Human | No |
| `tmp/**` | Transient artifacts | During task | Agent | N/A (gitignored) |
