# Benchmark Method

## Metrics

| Metric | Definition |
|--------|------------|
| Feature completion rate | Tasks meeting DoD without human rewrite |
| Regression rate | Bugs in neighboring tests after change |
| Integration failures | FE/BE contract mismatches found post-merge |
| Test failures escaped | Broken main after agent DONE |
| Security issues | Authz/injection findings post-review |
| Architectural violations | Layering/duplication |
| Unnecessary code changes | Files touched outside impact analysis |
| Token cost | Prompt+completion tokens |
| Agent handoffs | Count (should stay low under Architecture C) |
| Completion latency | Wall clock to verified DONE |

## Protocol

Run each task twice: **baseline** (no OS) vs **with OS** (adapters installed). Same model, same repo snapshot.

## Tasks (10)

1. Add a filtered list endpoint matching sibling pagination.
2. Add a field to an existing model + migrate safely.
3. Change an API response field consumed by React.
4. Fix a BOLA bug (user can read another's object).
5. Build a settings form with loading/error states.
6. Dockerize a Django+React app for `compose up`.
7. Refactor a fat view into service+repo without behavior change.
8. Investigate a flaky test.
9. Hotfix a 500 on a known endpoint (minimal diff).
10. Add Celery task with idempotency for email send.

## Scoring

For each task: 0–2 on correctness, integration, safety, diff hygiene, evidence. Prefer OS if total higher and token cost ≤ 1.5× baseline unless quality gap is large.
