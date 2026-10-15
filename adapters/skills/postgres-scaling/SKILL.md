---
name: postgres-scaling
description: Diagnose and fix PostgreSQL performance and scale — pg_stat_statements, EXPLAIN, N+1, indexes, pooling (PgBouncer), replicas, partitioning, and geo-sharding / data residency with the shahrah proxy. Use for slow queries, connection exhaustion, table growth, read scaling, or multi-region users.
---

# PostgreSQL performance & scaling

Follow `${CLAUDE_PLUGIN_ROOT}/skills/database/PostgresScalingSkill.md`.

Measure → queries → indexes → pooling → cache → replicas → partitioning → sharding. Attach before/after evidence (query count, p95, EXPLAIN). Multi-region trial stack: `${CLAUDE_PLUGIN_ROOT}/docker/shahrah/`; proxy source and docs: `${CLAUDE_PLUGIN_ROOT}/shahrah/`.
