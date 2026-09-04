# Skill: Token & Model Routing

```
Name: token-model-routing
Domain: architecture / cost
Purpose: Decide model tier and context load so small tasks stay cheap and leads use the highest model
Trigger: Every non-trivial session start; greenfield; before spawning reviewers; when user cares about cost/latency
Do Not Trigger: Mid-edit after tier already set for this task (unless escalating)
```

## Non-negotiables

1. **Classify tier before deep work** (T0–T3) using `standards/ModelRoutingMatrix.md`.
2. **Leads use Max (T3):** Security Reviewer, Architecture Reviewer, and orchestrator planning for Medium+ features.
3. **Workers match the task:** T0/T1 must not use T3 models when a cheaper model is configured.
4. **Existing `MODEL_ROUTING.md` wins** for concrete model IDs.
5. **Don't spawn expensive reviewers** for T0/T1 unless security surface appears.
6. Prefer **deterministic tools** over another LLM pass (lint/test > “please review style”).

## Procedure

1. Read `project-context/MODEL_ROUTING.md` (create from template if missing).
2. Classify task → T0/T1/T2/T3.
3. State in one line: `Routing: T1 (standard) — single endpoint sibling; no reviewers.`
4. Select model alias for implementer; if you are the only session, still **limit skills/gates** to that tier.
5. If tool supports subagents with `model`: set Security/Architecture agents to **max** alias.
6. Escalate one tier after 2 failed verify loops; never infinite T3 loops.

## Anti-patterns

- Flagship model for renaming a variable
- Spawning 3 review agents for a padding fix
- Loading all of `skills/mobile/` for a CSS change
- Skipping Security Reviewer on IAP “to save tokens”

## Expected output

```text
Routing: T2 | implementer=strong | reviewers=security@max | skills≤3 | gates=matrix:FE+BE
```

## Related

`ModelRoutingMatrix`, ProgressiveDisclosure, OrchestratorSpec, QualityGateMatrix
