# Performance Investigation Workflow

Optimize from evidence, not fashion.

## Flow

```
Define SLO / user-visible symptom
    → Reproduce with measurement
    → Identify bottleneck (DB, CPU, network, render)
    → Fix smallest cause
    → Re-measure
    → Guardrail test if possible
```

## Backend Checks

- Query count / N+1 / missing indexes
- Serialization of unused fields
- Cache correctness and invalidation
- Connection pool saturation
- Sync work that should be a job

## Frontend Checks

- Bundle size / unused imports
- Waterfalls vs parallel fetch
- Unnecessary re-renders
- Images (size, format, lazy)
- Code splitting for routes

## Forbidden

- Adding Redis "because scale" without evidence
- Microservices as a performance fix
- Caching without invalidation plan

## Skills

- `performance`
- `observability` if missing metrics
