# Skill: PostgreSQL Performance & Scaling

```
Name: postgres-scaling
Domain: database / performance
Purpose: Make PostgreSQL fast and scalable with evidence — queries, indexes, pooling, replicas,
         partitioning, sharding, and data residency — in that order
Trigger: Slow queries, N+1, connection exhaustion, high DB CPU/IO, table growth, read scaling,
         multi-region users, data-residency requirements, "optimize the database"
Do Not Trigger: Schema migrations without a performance question (use migration-review)
```

## Order of operations (stop at the first step that fixes it)

```
measure → fix queries → index → pool connections → cache → read replicas → partition → shard / geo-route
```

Each step costs more operational complexity than the last. Sharding a database that needed one index is a failure.

## 1. Measure

- Enable `pg_stat_statements` (the compose templates do) and rank by `total_exec_time` and `mean_exec_time`.
- `EXPLAIN (ANALYZE, BUFFERS, SETTINGS)` the top offenders on production-like data volumes.
- App side: count queries per request (Django `assertNumQueries`, `django-debug-toolbar`, OpenTelemetry DB spans).
- Watch: connections in use vs `max_connections`, cache hit ratio, autovacuum lag, replication lag, bloat.

## 2. Queries

- Kill N+1: `select_related` / `prefetch_related` (Django), `include`/joins (Prisma/Drizzle), DataLoader for GraphQL.
- Keyset (cursor) pagination for deep lists instead of large `OFFSET`.
- Select only needed columns; avoid `COUNT(*)` on every list page (estimate or cache).
- Batch writes (`bulk_create`, `COPY`), and keep transactions short.

## 3. Indexes

- B-tree for equality/range; composite in selectivity order matching `WHERE` + `ORDER BY`.
- Partial indexes for hot subsets (`WHERE deleted_at IS NULL`), covering (`INCLUDE`) for index-only scans.
- GIN for `jsonb`/full-text/trigram; BRIN for huge append-only time series; `pgvector` HNSW for embeddings.
- PostgreSQL 18 adds B-tree **skip scan**, so a composite index can serve queries that omit its leading column — re-check before adding near-duplicate indexes.
- Create on live tables with `CREATE INDEX CONCURRENTLY` (Django: `AddIndexConcurrently`, non-atomic migration). Drop unused indexes (`pg_stat_user_indexes.idx_scan = 0`) — they slow writes.

## 4. Connections

- App-side pool sized to cores, not to traffic (Django 5.1+ `OPTIONS: {"pool": True}` with psycopg 3, or `CONN_MAX_AGE` + `CONN_HEALTH_CHECKS`).
- Many app replicas or serverless → external pooler: **PgBouncer** in transaction mode (compose profile `pooler`), or **shahrah** when you also need routing (below). Transaction pooling breaks session state: no session-level advisory locks, `SET`, or server-side cursors across transactions; use protocol-level prepared statements only with a pooler that supports them.

## 5. Cache

Redis/Valkey for computed or hot read models with explicit TTL **and** invalidation on write. Never cache authorization decisions without the user in the key.

## 6. Read replicas

- Route read-only, staleness-tolerant queries to replicas; read-your-writes paths stay on the primary.
- Django: database router; or let a proxy split reads/writes (shahrah does, by statement analysis).
- Monitor replica lag and fail reads back to the primary above a threshold.

## 7. Partitioning

Declarative partitioning (range by time, list by tenant/region, hash) when tables reach hundreds of millions of rows or need cheap retention (`DETACH PARTITION` instead of mass `DELETE`). Every query must carry the partition key to prune.

## 8. Sharding & multi-region — when, and with what

Shard only when one primary cannot hold the write load or the data must live in specific regions.

| Need | Option |
|------|--------|
| Pooling only | PgBouncer |
| Pooling + read/write split + hash sharding behind one endpoint | shahrah, PgDog, pgcat, Citus (extension) |
| **Users' rows must live in their region** (residency, latency), move users between regions online | **shahrah** — region directory in front of the shard map |
| Fully managed distributed SQL | Cloud vendor offerings (trade portability) |

### shahrah (bundled in `rigor-os/shahrah/`, upstream `rs-alireza/shahrah`)

A Rust PostgreSQL wire-protocol proxy: applications keep their normal driver/ORM.

- **Declare every table** in the topology: `[policy.keys.<table>]` (geo-partitioned by one key: `int | text | uuid`) or `[policy.replicated.<table>]` (same rows everywhere, one `writer_region`). Undeclared or key-less statements are **refused**, not guessed.
- Statements must carry the shard key; for views/joins/ORMs that hide it, add a hint comment: `/* shahrah: key=7 */ select …` (Python helper: `shahrah.hints.by_key`).
- Console (`psql … shahrah`, simple protocol only): `WHERE IS users 100005`, `SHOW POOLS|HEALTH|TOPOLOGY|DIRECTORY`, `RELOCATE users 100005 TO eu-central`, `REPAIR`, `REBALANCE`.
- Security defaults to keep: metrics/dashboard bound to loopback unless `SHAHRAH_METRICS_PASSWORD` is set; set `SHAHRAH_BACKEND_TLS=require` across networks (unset means **disable**); client TLS via `SHAHRAH_TLS_CERT/KEY`.
- Source and docs: `rigor-os/shahrah/README.md`, shard math in `rigor-os/shahrah/docs/SHARDS.md`, measured numbers in `rigor-os/shahrah/docs/NUMBERS.md`.
- Local trial: `docker/shahrah/compose.yml` (builds the proxy from the bundled source). Production: one topology file per fleet, Raft group (`SHAHRAH_RAFT_*`) for >1 proxy, Prometheus on `/metrics`.
- Design implications for the app: choose the shard key early (usually tenant/user id), keep cross-key joins out of hot paths, make global reference tables `replicated`.

## Anti-patterns

- Adding indexes without reading the plan; indexing every column
- Raising `max_connections` to 2000 instead of pooling
- Sharding before fixing N+1
- Cross-shard transactions in request paths
- Caching without invalidation; replicas for read-your-writes flows

## Evidence (attach before DONE)

```text
DB:
  before: GET /api/orders p95 840ms, 63 queries   (pg_stat_statements top-1: 41% total time)
  change: prefetch_related(items) + index orders(customer_id, created_at DESC)
  after:  p95 95ms, 4 queries; EXPLAIN shows Index Scan, Buffers shared hit=…
```

## Related

`migration-review`, `performance`, `observability`, `docker` (pooler/geo overlays), `MigrationReviewSkill`
