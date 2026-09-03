# Skill: Test Strategy

```
Name: test-strategy
Domain: testing
Purpose: Choose the right test level and avoid theater coverage
Trigger: New behavior, bug fixes, API changes
Do Not Trigger: Pure copy/docs
```

## Procedure

1. Identify the behavior the user will notice.
2. Unit-test domain/service rules.
3. Integration-test persistence and HTTP adapters.
4. Contract-test public APIs.
5. E2E only the critical user path for medium/large features.

## Related

`testing-gate`, `flaky-test-investigation`
