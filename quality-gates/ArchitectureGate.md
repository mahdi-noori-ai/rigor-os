# Architecture Gate

## Checks

1. **Sibling pattern.** New code matches the cleanest existing pattern in that app.
2. **Layering.** Presentation does not own business rules or ORM. Application/services do not call `Model.objects` if the project uses repositories.
3. **Dependencies point inward.** Domain does not import HTTP/ORM frameworks when the project already isolates them.
4. **No duplicate abstractions.** Reuse existing services/repos/use cases.
5. **YAGNI.** No new microservice, event bus, or CQRS because it is fashionable.
6. **API boundaries.** Public contracts versioned or additive; no silent breaking changes.
7. **Cohesion.** Change lives in the owning module, not a new catch-all util dump.

## Layering Table (Django overlay default)

| Layer | May do | Must not do |
|-------|--------|-------------|
| View | Auth, validate, DTO, resolve use case, map response | Business rules, ORM, multi-step workflows |
| Service / UseCase | Orchestration, transactions, rules, call ports | Raw HttpRequest, `Model.objects` |
| Repository | Persistence, querysets, mapping | Cross-domain policy |
| Interface | Ports | Concrete Django in Protocol if app avoids it |

If the project is not layered, **do not impose this table**. Follow what exists.

## Fail the gate if

- Fat views with ORM + business rules
- New parallel helper duplicating a service
- Shared method signature changed for one caller
- Unrelated rewrite of architecture

## YAGNI Default

Monolith or modular monolith until operational evidence requires split.
