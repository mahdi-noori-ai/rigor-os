# Skill: Performance

```
Name: performance
Domain: performance
Purpose: Evidence-based performance work
Trigger: Slow endpoints, N+1, large payloads, poor Core Web Vitals, "optimize this"
Do Not Trigger: Premature optimization on cold code without a problem
```

## Backend

Query counts, indexes, pagination, select_related/prefetch, cache with TTL+invalidation, serialization cost, connection pools. Database depth: `skills/database/PostgresScalingSkill.md`.

## Frontend

Core Web Vitals at the 75th percentile on mobile: **LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1** (field data from CrUX/RUM beats lab numbers).
Renders, bundle size budgets, request waterfalls, image formats/sizes (`fetchpriority="high"` on the LCP image), code split, server components/SSR for content routes, memo only when the profiler shows need (React Compiler handles most memoisation where enabled).

## Infra

CPU/mem, worker concurrency, DB connections vs app replicas.

## Procedure

Measure → hypothesize → smallest fix → remeasure.
