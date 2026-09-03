# Production Incident / Hotfix Workflow

Speed with discipline. Do not make the outage worse.

## Flow

```
Stabilize (mitigate user harm)
    → Gather evidence (logs, traces, metrics, last deploy)
    → Identify blast radius
    → Minimal hotfix OR rollback
    → Verify in production
    → Regression test
    → Post-incident note if significant
```

## Rules

1. Prefer rollback if the last deploy is the likely cause and rollback is safe.
2. Hotfix must be the smallest change. No refactors.
3. Do not run untested migrations in panic.
4. Do not disable auth "temporarily."
5. Communicate BLOCKED if you cannot reproduce and lack evidence.

## After Mitigation

- Add a test that would have caught this.
- Check whether the failure belongs in a new rule, skill, or deterministic gate (`evolution/FrameworkEvolution.md`).
