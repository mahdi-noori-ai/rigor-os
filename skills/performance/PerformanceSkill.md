# Skill: Performance

```
Name: performance
Domain: performance
Purpose: Evidence-based performance work
Trigger: Slow endpoints, N+1, large payloads, poor Core Web Vitals, "optimize this"
Do Not Trigger: Premature optimization on cold code without a problem
```

## Backend

Query counts, indexes, pagination, select_related/prefetch, cache with TTL+invalidation, serialization cost, connection pools.

## Frontend

Renders, bundle, waterfalls, images, code split, memo only when profiler shows need.

## Infra

CPU/mem, worker concurrency, DB connections vs app replicas.

## Procedure

Measure → hypothesize → smallest fix → remeasure.
