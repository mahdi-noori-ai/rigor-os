# Skill: Migration Review

```
Name: migration-review
Domain: database
Purpose: Production-safe schema and data migrations
Trigger: New models, fields, indexes, data backfills, Django/Alembic/Prisma migrations
Do Not Trigger: Query-only changes with no schema diff
```

## Checks

- Additive vs destructive
- `NOT NULL` without default on populated tables
- Index creation strategy (locks)
- FK `on_delete`
- Data migration batching
- Expand/contract for rolling deploys
- Rollback documented
- Large table: estimate row count if possible

## Procedure

1. Read generated migration; do not blindly accept autogen.
2. Split data vs schema if mixed.
3. Ensure previous app version still runs (or require downtime approval).
4. Test migrate + migrate reverse (if reversible) locally.

## Anti-patterns

- Dropping columns the old code still reads
- Unbounded `RunPython`
- Unique constraint on dirty data without cleanup
