# Skill: Code Review

```
Name: code-review
Domain: review
Purpose: Distinct review perspectives without duplicate generic comments
Trigger: PR review, pre-merge, user asks for review
```

## Modes (pick relevant, don't run all as separate agents)

| Mode | Looks for |
|------|-----------|
| Correctness | Logic, edge cases, error handling |
| Architecture | Layers, duplication, YAGNI |
| Maintainability | Naming, complexity |
| Security | OWASP, secrets |
| Performance | N+1, payloads |
| Tests | Real assertions, no theater |
| Frontend | States, responsive, a11y |

One review pass may combine modes in a single structured report. Avoid five agents repeating "add comments."
