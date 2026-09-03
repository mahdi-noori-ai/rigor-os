# Skill: Contract Integrity

```
Name: contract-integrity
Domain: API
Purpose: Keep backend, OpenAPI, and frontend consumers in lockstep
Trigger Conditions: API schema, serializer, status code, auth, or client types change; FE+BE features
Do Not Trigger When: Pure CSS, docs-only, internal refactor with no public contract change
```

## Required Context

Project OpenAPI location (`schemas.py`, `openapi.yaml`). Frontend client/types path. Pagination conventions.

## Procedure

1. Locate sibling endpoint schema and copy conventions.
2. Update server implementation and schema together.
3. Classify change: additive vs breaking (`workflows/APIChange.md`).
4. Lint spec if tools exist (Spectral).
5. Diff against previous spec.
6. Regenerate or update TypeScript types.
7. Add/adjust API tests asserting status + body shape.
8. Hit real endpoint once (test client or compose).

## Checks

- Request/response/status/auth/permissions documented and implemented
- Frontend types compile
- Error shape matches project (do not invent `{success,data,error}` if unused)

## Common Failure Patterns

- Backend ships new field; UI still uses old client
- Status 204 vs 200 mismatch
- Pagination keys renamed
- Mocked frontend tests pass while live API 403s

## Expected Output

Updated spec + client + passing contract/API tests + evidence of one live round-trip.

## Related Skills

`api-engineer`, `impact-analysis`, `frontend-ui-quality`
