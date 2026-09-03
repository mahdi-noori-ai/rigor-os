# API Change Workflow

Highest priority for preventing frontend/backend drift.

## Trigger

Any change to request/response schema, status codes, auth, permissions, pagination, or URL.

## Flow

```
Identify consumers → Update backend (view/serializer/schema)
    → Update OpenAPI / schemas.py
    → Diff contract (breaking vs additive)
    → Update frontend types + client
    → Update loading/error handling if statuses change
    → Tests (API + contract + consumer)
    → Integration verification (real HTTP)
    → Docs
```

## Breaking vs Additive

| Change | Type | Action |
|--------|------|--------|
| New optional field | Additive | Safe if clients ignore unknown |
| New required request field | Breaking | Version or coordinate FE+BE deploy |
| Remove/rename field | Breaking | Deprecate first or ship together |
| Change type/enum | Breaking | Coordinate |
| New error status | Possibly breaking | Update FE error handling |
| Auth requirement added | Breaking | Coordinate |

## Must Verify

- Request schema
- Response schema
- Status codes
- Validation messages (project shape)
- Authentication
- Permissions (object + function level)
- Frontend types
- API client
- Loading/failure behavior
- Tests
- Documentation

A feature requiring frontend + backend is **not complete** until real integration is verified — not mock-only.

## Skills

- `api-engineer`
- `contract-integrity`
- `impact-analysis`
- Frontend API integration if UI consumes the API
