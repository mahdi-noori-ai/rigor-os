# Skill: Flaky Test Investigation

```
Name: flaky-test-investigation
Domain: testing
Purpose: Fix nondeterministic tests instead of hiding them
Trigger: Tests that fail intermittently, CI red then green
Do Not Trigger: Deterministic failing tests (that's BugFix)
```

## Procedure

1. Reproduce with repeated runs.
2. Isolate: time, order, shared DB, network, threads, random.
3. Make hermetic: fakes, transactional tests, frozen time.
4. Re-run to confirm stability.
5. Never skip as the fix.

## Common causes

- Missing `select_for_update` tests racing
- Unordered list assertions
- Real sleep()
- Shared module globals
