---
name: stack-selection
description: Choose language, framework, and tools from project type when the user does not specify a stack. Use for greenfield apps, web vs game vs LLM products, or empty repos. Never override an existing project stack.
---

# Stack selection

Follow `${CLAUDE_PLUGIN_ROOT}/workflows/StackSelection.md` and:

- `${CLAUDE_PLUGIN_ROOT}/skills/architecture/StackSelectionSkill.md`
- `${CLAUDE_PLUGIN_ROOT}/standards/DefaultStackMatrix.md`

1. Existing repo stack → match it (stop).
2. User named stack → use it.
3. Else classify type → apply matrix defaults → write `project-context/STACK_DECISION.md` → announce override option → continue bootstrap/feature work.

Defaults favor Django+DRF, React/Next, PostgreSQL, Docker Compose, Kotlin/Compose or Unity for mobile games, Python for LLM apps.
