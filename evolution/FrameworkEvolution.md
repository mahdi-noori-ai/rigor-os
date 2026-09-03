# Framework Evolution

When the agent repeats a mistake, choose the **smallest durable fix**.

## Decision tree

```
Is a compiler/linter/test able to catch it forever?
  YES → Add deterministic check (Ruff rule, test, schema, hook)
  NO ↓
Is it a universal non-negotiable?
  YES → Short Rule (constitution / alwaysApply / safety)
  NO ↓
Is it a procedure for a task type?
  YES → Skill or Workflow step
  NO ↓
Is it project-specific fact?
  YES → project-context / ADR
  NO ↓
Is it rare and judgment-heavy?
  YES → Quality gate checklist item or review agent note
```

## Lifecycle

1. **Add** with owner + date + example failure.
2. **Review** quarterly: merge duplicates, delete obsolete.
3. **Version** the OS (`CHANGELOG` optional). Adapters regenerated via `sync-adapters.sh`.
4. Prefer deleting a rule that is unused over accumulating encyclopedia prompts.

## Anti-pattern

Endless new Markdown for every incident. Prefer one good test.
