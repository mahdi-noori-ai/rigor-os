---
name: token-model-routing
description: Route tasks to economy vs max models and limit context by complexity. Use at session start, before spawning reviewers, or when saving tokens — T0/T1 cheap; orchestrator/security/architecture use max.
---

# Token & model routing

Follow `${CLAUDE_PLUGIN_ROOT}/workflows/TaskRouting.md` and:

- `${CLAUDE_PLUGIN_ROOT}/skills/architecture/TokenModelRoutingSkill.md`
- `${CLAUDE_PLUGIN_ROOT}/standards/ModelRoutingMatrix.md`
- `rigor-os/project-context/MODEL_ROUTING.md`

Announce: `Routing: T# | implementer=… | reviewers=…@max | skills≤N`.

Never use max model for typos. Never skip Security Reviewer on IAP/auth to “save tokens.”
