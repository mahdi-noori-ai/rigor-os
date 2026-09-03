# Skill: Backend Quality

```
Name: backend-quality
Domain: backend
Purpose: Keep backend code layered, testable, and consistent
Trigger: New services, repos, domain logic, DI, Python/Django/FastAPI backend work
Do Not Trigger: Frontend-only, infra-only
```

## Non-negotiables

1. Match existing structure and culture.
2. Reuse; do not rewrite shared helpers for one use case unless asked.
3. New code looks like old good code in that app.
4. Prefer the newest layered examples if the app mixes styles.
5. Run the project's linter (Ruff for Python) on changed files.

## Generic layering (adapt to the repo)

```
presentation → application → domain → data
```

Service/use case layer should be persistence-API-free when the project uses repositories.

## DI

If the project uses injector/ports: depend on interfaces, bind in existing injector modules, resolve like neighbors (`@inject` + `injector_instance.get` when that is the pattern).

External HTTP belongs in adapters, not views.

## Tests

Every new/changed service: `test_*_service.py`, happy + validation paths, existing fixtures.

## Anti-patterns

- Fat views
- ORM in services when repos exist
- Duplicate helper modules
- Breaking shared signatures
- Shipping without service tests
