# Skill: Architecture

```
Name: architecture
Domain: architecture
Purpose: Protect modularity, boundaries, and simplicity
Trigger: New modules, cross-app features, new services, significant refactors
Do Not Trigger: Local bugfix following existing pattern
```

## Concerns (apply only when relevant)

Modularity, cohesion/coupling, layering, domain modeling, API boundaries, sync vs async, caching, queues, transactions, idempotency, retries/timeouts, versioning, backward compatibility.

## Non-negotiables

- Do not introduce complexity because a pattern is fashionable.
- YAGNI: monolith/modular monolith until evidence requires otherwise.
- Dependency direction: domain inward.
- Idempotency for retried jobs and webhooks.

## Procedure

1. Draw (briefly) the current data flow for the feature.
2. Place logic in the owning bounded context.
3. Choose sync HTTP unless the work is inherently async (email, bills, long jobs).
4. If introducing a queue: define retry, idempotency key, and failure visibility.
5. Recommend ADR only for decisions that future agents must not reverse casually.

## Anti-patterns

- Premature microservices
- Shared database as integration for new services
- Caching without invalidation
- Distributed transactions without a saga/outbox the project already has
