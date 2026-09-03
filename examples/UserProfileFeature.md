# Example: User Profile Management Feature

Realistic walkthrough of Architecture C (hybrid orchestrator + skills + gates).

## User request

> Add user profile management with backend API, frontend forms, authentication/authorization, validation, and database changes.

## Orchestrator summary (not chain-of-thought)

| Decision | Choice |
|----------|--------|
| Workflow | FeatureImplementation |
| Profile | Medium |
| Domains | DB, Backend, API contract, Frontend, Security |
| Sibling | Existing user/auth endpoints |
| Agents beyond self | SecurityReviewer after implement |
| ArchitectureReviewer | Optional (new fields only) — skip if following sibling layout |

## Skills selected

1. `impact-analysis`
2. `django-clean-architecture` (overlay)
3. `api-engineer` + `contract-integrity`
4. `migration-review`
5. `frontend-ui-quality` + `ui-design-quality` + `accessibility`
6. `appsec-review`
7. `test-strategy`

## Task decomposition

1. Model fields (bio, avatar, display_name) + migration (additive, nullable first).
2. `IProfileRepository` + repo methods.
3. `UpdateProfileService` / use case with validation (ORM-free).
4. DI bindings.
5. Views/serializers/schemas for `GET/PUT /api/v1/users/me/profile/`.
6. Service tests + API tests for 401/403/400/200.
7. OpenAPI update; regenerate TS types.
8. Profile form UI with loading/empty/error; reuse design tokens.
9. IntegrationVerification (real HTTP).
10. SecurityReviewer for BOLA (cannot PUT another user's id).
11. DoD evidence package.

## Implementation order

```
migration → repo → service → API → tests → contract → FE types → UI → integration → security review → DONE
```

## Integration points

- Serializer fields ↔ OpenAPI ↔ TS types ↔ form fields
- Auth: same session/JWT as siblings
- Permissions: `IsAuthenticated` + object is always "me" (no foreign id) OR ownership check if id in path

## Tests

- Service: valid update, validation errors
- API: unauthenticated 401; cannot update other user
- FE: form validation; server error mapping (optional unit)
- Contract: response schema matches

## Review gates

| Gate | Result needed |
|------|----------------|
| ArchitectureGate | Layering OK |
| TestingGate | Service + API green |
| IntegrationVerification | Live GET/PUT OK |
| SecurityGate | API1/API3/API5 checked |
| UI | 375/768/1280 + empty avatar state |
| DoD | Evidence attached |

## Definition of Done evidence (example)

```
ruff check src/apps/users → clean
pytest apps/users -q → 18 passed
openapi types regenerated
manual: PUT /api/v1/users/me/profile/ 200; other user 403
UI: profile form OK at 375px and 1280px
SecurityReviewer: PASS
```
