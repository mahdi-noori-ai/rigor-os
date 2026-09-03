# Refactor Workflow

Safeguards for AI-driven refactors. Behavior must be preserved.

## Preconditions

- Baseline tests exist and pass. If not, add characterization tests first — do not refactor untested code without user approval.
- Scope is named and bounded (one module, one layer, one pattern).
- Public API compatibility assessed.

## Rules

1. **Behavior preservation.** Same inputs → same outputs (including error types).
2. **Incremental.** One coherent step at a time; tests green between steps.
3. **No feature work** mixed into the refactor.
4. **No unrelated formatting** unless the project formatter is the only change and user asked.
5. **Dependency impact.** Callers, DI bindings, imports, serializers, URLs.
6. **Performance.** Do not silently worsen query counts or payload size.

## Flow

```
Baseline tests → Scope lock → Incremental extract/move
    → Tests after each step → Public API check → Lint → Review architecture if large
```

## Forbidden

- Rewriting working systems without justification
- Introducing microservices or new frameworks as a "refactor"
- Changing response shapes as a side effect
- Skipping tests because "it's just a move"

## Completion

- Baseline tests still pass
- New structure matches sibling patterns
- Diff reviewable (not a 2000-line mixed rewrite)
