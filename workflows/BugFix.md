# Bug Fix Workflow

Prefer root-cause fixes over symptom patches.

## Flow

```
Reproduce → Gather evidence → Root cause → Affected systems
    → Regression test → Minimal correct fix → Verify → Neighboring behavior → Document if significant
```

## Steps

1. **Reproduce.** Fail without a failing test or log/trace when possible. Write the test first if the bug is deterministic.
2. **Evidence.** Stack traces, request IDs, query logs, screenshots, failing test output — not guesses.
3. **Root cause.** Identify the actual defect (wrong query, missing auth, race, bad default). Do not patch symptoms (try/except swallow, skip test, extra CSS hack that hides a layout bug).
4. **Impact.** Which callers, APIs, jobs, UI screens break if you change this?
5. **Regression protection.** Add or identify a test that would have caught this.
6. **Minimal fix.** Smallest change that addresses root cause. Match existing patterns.
7. **Verify.** Run the new test + neighboring tests. Lint changed files.
8. **Document** only if the root cause is surprising or operational (runbook, ADR).

## Anti-Patterns

- Commenting out failing tests
- Broadening mocks until tests pass
- Catching Exception and returning 200
- Rewriting the module "while we're here"
- Claiming fixed without reproduction evidence

## Skills

- Domain skill for the affected layer
- Flaky test investigation if the bug is intermittent
- Security review if the bug is an auth/data leak
