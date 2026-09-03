# Skill: API Engineer

```
Name: api-engineer
Domain: backend
Purpose: Design and implement HTTP APIs that match existing conventions
Trigger: New or changed REST endpoints, serializers, errors, pagination, filtering
Do Not Trigger: Non-HTTP work, UI-only
```

## Non-negotiables

1. Copy sibling endpoint shapes before inventing a body.
2. Thin views: validate → DTO → service → response serializer.
3. Document in co-located schema (OpenAPI / `schemas.py`).
4. Pagination uses the project's keys (default example: `current`, `page_count`, `page_size`, `count`, `next`, `previous`, `results`).
5. Writes accept FK ids when siblings do; reads may nest display objects when siblings nest.

## Responsibilities

| Concern | Do | Don't |
|---------|----|-------|
| Validation | Serializer/schema at boundary | Trust client JSON blindly |
| Errors | Project exception types and status mapping | Random 500 with stack in prod |
| Auth | Same permission classes as siblings | Forget object-level checks |
| Versioning | Follow existing `/v1/` layout | Mix v1 and unversioned |

## Workflow

1. Find sibling endpoint folder (`views`, `serializers`, `schemas`).
2. Trace view → service → repo.
3. Align request/response naming (`*RequestSerializer` / `*ResponseSerializer` if that is the culture).
4. Wire URLs like siblings.
5. Tests for happy + authz + validation.

## Anti-patterns

- New global envelope
- Business rules in the view
- Undocumented 201 vs 200 inconsistency

## Related

`contract-integrity`, `backend-quality`, Django overlay
