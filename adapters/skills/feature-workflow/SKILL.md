---
name: feature-workflow
description: Implement a significant product feature end-to-end. Use when the user asks to build a feature, capability, or product slice spanning backend, frontend, or database.
---

# Feature workflow

Follow `${CLAUDE_PLUGIN_ROOT}/workflows/FeatureImplementation.md`.

1. Inspect sibling patterns and project-context.
2. Write acceptance criteria.
3. Impact analysis (`${CLAUDE_PLUGIN_ROOT}/skills/impact-analysis/`).
4. Implement in order: data → application → API → contract → UI → tests.
5. Quality gates + Definition of Done with evidence.
6. Max 3 verify/fix loops; then BLOCKED.
