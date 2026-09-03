# Database Migration Workflow

Migrations require special review. Local success ≠ production safety.

## Flow

```
Schema intent → Constraints/indexes → Backward compatibility
    → Write migration → Review → Test locally
    → Rollback plan → Deploy order vs app code
```

## Required Checks

1. **Additive first.** Add columns/tables as nullable or with defaults before making required.
2. **No destructive ops** on large tables without explicit approval (`DROP COLUMN`, type changes that rewrite tables).
3. **Indexes.** Concurrent/online where the DB supports it for production tables.
4. **Foreign keys** and `ON DELETE` behavior match domain rules.
5. **Data migrations** separate from schema when possible; batched for large tables.
6. **Rollback.** How to reverse? If irreversible, document and get approval.
7. **Expand/contract.** App code must work with both old and new schema during rolling deploys.
8. **Backups.** Confirm restore path exists before destructive production migrations.

## Anti-Patterns

- `RunPython` that iterates millions of rows in one transaction
- Removing a column the previous app version still reads
- Adding `NOT NULL` without default on populated table
- Ignoring lock time on large tables

## Skills

- `migration-review`
- Architecture gate if domain model changes
