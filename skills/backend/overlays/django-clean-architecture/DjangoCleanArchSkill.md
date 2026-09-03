# Skill: Django Clean Architecture Overlay

```
Name: django-clean-architecture
Domain: backend / Django
Purpose: Mandatory layering, DI, API style, and testing for Django/DRF projects that already use this culture
Trigger: Python/Django/DRF work in a layered app (presentation/application/domain/data)
Do Not Trigger: Non-Django repos; apps that clearly use fat models/views only — then match THAT culture instead
```

Adapted from production backend guidelines (sodoor-style). Do not invent a parallel style.

## Non-negotiables

1. Match existing codebase structure and culture before writing anything.
2. Reuse, do not rewrite. Do not change shared helpers for a new use case unless asked.
3. New code must look like old good code — naming, folders, response shapes, error types, DI.
4. Prefer the cleanest existing pattern; if mixed, follow newest layered examples (view → service/use case → repository + interfaces).
5. **Service/use case layer must be ORM-free.** No `Model.objects...` in services; put queries in repository methods.
6. **Every change must pass Ruff.** `ruff check` on changed Python files before finalizing.

## Canonical layout

```
src/apps/<app>/v1/
  presentation/api/<endpoint>/{views,serializers,schemas}.py
  presentation/urls/
  application/services/  |  application/usecases/
  domain/{interfaces,dtos|dto,entities,services}/
  data/{models,repositories,migrations}/
```

Exceptions: some apps keep layers at app root with `presentation/v1/`. Follow that app when working there.

### Responsibilities

| Layer | May do | Must not do |
|-------|--------|-------------|
| **View** | Auth/permissions, validate request serializer, build DTO/command, resolve service/use case, map output serializer, return `Response` | Business rules, ORM queries, multi-step workflows |
| **Service / UseCase** | Orchestration, transactions, validation rules, call repos/ports | Fat HTTP concerns, raw request objects, direct `Model.objects` queries |
| **Repository** | Persistence, querysets, prefetch, map to entities/DTOs when the app already does | Cross-domain business policy |
| **Interface (`I*` / Protocol)** | Ports for repos and external systems | Concrete Django imports in Protocol when the app avoids them |
| **DTO** | Boundary payloads (`*CommandDTO`, `*InputDTO`, `*OutputDTO`) | Leaking `HttpRequest` into domain |
| **Adapter** | Implement a port by calling another app/core adapter | Spreading foreign-app imports across the feature |

Shared infra: `src/core/` (`injectors`, `adapters`, `mixins`, `paginations`, `exceptions`, `serializers`) when present.

## Dependency injection

- Prefer `@inject` on `__init__` and resolve with `injector_instance.get(...)`.
- Depend on **interfaces**, not concrete repos, for new cross-cutting or testable services.
- Bind in the app’s `*InjectorModule` (`binder.bind(IFoo, to=FooImpl)`).
- Register modules in `src/core/injectors/` (`repository_injector`, `service_injector`, `use_case_injector`, `gateway_injector`).
- External systems go through `core/adapters` or app adapters implementing a port — do not call vendor HTTP from views.

## Views & serializers

- One endpoint folder: `views.py` + `serializers.py` + `schemas.py` (OpenAPI).
- Thin views: validate → DTO → service/use case → response serializer.
- Naming: `*RequestSerializer` / `*InputSerializer`, `*ResponseSerializer` / `*OutputSerializer`.
- Wire URLs the same way as sibling endpoints.

## Repositories & models

- Repos under `data/repositories/` (or that app’s existing location).
- Prefer `DataModelRepoMixins` + `model = ...` and matching `I*` from `domain/interfaces/`.
- Raise the same custom exceptions (`CustomObjectDoesNotExistError`, `CustomValidationError`, etc.).
- DB-backed validation in services must call a repository method, not direct ORM.

## API response style

- **Create** often returns `{"id": ...}` when siblings do.
- **Empty success** often returns `Response("OK")` when siblings do.
- **Read/detail/list** use output serializers; nested objects for display when siblings nest.
- **Writes** usually accept FK **ids**; do not invent a new envelope.
- **Pagination** must use `BasePagination` keys: `current`, `page_count`, `page_size`, `count`, `next`, `previous`, `results`.
- No new global `{success, data, error}` wrapper unless the family already uses one.

## Tests (required for services)

- Add/update tests for every new or changed service (and use case when that is the entry point).
- Place tests next to the layer: `domain/tests/`, `application/tests/`.
- Files: `test_*_service.py`; methods: `test_<behavior>_...`.
- Prefer existing fixtures/factories. Use DI/fixtures like neighboring tests.
- Cover happy path + important validation/error paths.

## Comments

- Prefer clear names. Short comments for invariants/adapters.
- Unfinished work: `# TODO(owner): ...`
- Do not leave large commented-out blocks.

## Implementation workflow (every task)

1. Find a sibling feature; mirror folder/layout/naming.
2. Trace view → service/use case → repo/interface; do not skip layers.
3. Reuse existing services/methods; extend without breaking callers.
4. Align serializers with existing API style.
5. Wire DI/bindings for new injectable types.
6. Write service tests; run relevant tests.
7. Run `ruff check` on changed Python files.
8. Keep the diff focused.

## Anti-patterns (reject)

- Fat views with ORM or business rules
- Direct ORM in service/use case (`InsuranceType.objects...` inside service)
- Parallel helper modules duplicating a service
- Changing shared methods’ behavior/signature for one feature
- Inconsistent response shapes vs siblings
- Skipping interfaces/DI where the area already uses them
- Shipping service changes without tests
