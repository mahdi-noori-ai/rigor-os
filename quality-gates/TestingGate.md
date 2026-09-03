# Testing Gate

## Hierarchy (Google-inspired mix)

Aim approximately: **80% small/unit**, **15% integration**, **5% E2E**. Adjust for architecture — APIs need more integration than a CLI.

| Size | Purpose | When mandatory |
|------|---------|----------------|
| Unit | Domain/service behavior | Every new/changed service or use case |
| Integration | DB, HTTP, queues together | Persistence, API endpoints, jobs |
| Contract | Spec vs live responses | Public API changes |
| E2E | Real user flow | Cross-domain features (medium/large) |
| Smoke | Deploy health | Releases |
| Performance | Latency/throughput | Hot paths with evidence of need |

## Required Behavior

1. Add/update tests for **every new or changed service** (and use case entry point).
2. Place tests next to the layer when the project already does (`application/tests/`, `domain/tests/`).
3. Prefer existing fixtures/factories. Mock only as neighboring tests do.
4. Cover happy path + important validation/error paths.
5. Test via public APIs of the unit under test — not private internals.

## Forbidden

- Modifying tests solely to make them pass without fixing production code
- Skipping or commenting out failing tests without written justification
- Excessive mocking that never exercises real behavior
- Hiding flaky tests (`xfail` without ticket, retries as the only fix)
- Claiming coverage that does not assert behavior

## Flaky Test Investigation

1. Run the test N times locally (`pytest --count=10` or equivalent).
2. Classify: time, order, network, shared state, clocks, random.
3. Fix root cause (isolation, fake clock, hermetic DB).
4. Do not merge with `flaky` marks unless user accepts and a ticket exists.

## Evidence

Gate passes only with command output: test runner exit 0 for the relevant subset.
