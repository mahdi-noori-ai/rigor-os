# Integration Verification

A feature spanning frontend and backend is **not complete** until the real integration is verified.

## Contract Pipeline

1. **Source of truth:** OpenAPI (or project's `schemas.py` / generated spec).
2. **Static:** Spec validates (Spectral / openapi-cli).
3. **Diff:** `oasdiff` (or equivalent) vs previous spec — fail on accidental breaking changes.
4. **Server:** Responses conform to schema (pytest + schemathesis or DRF schema tests).
5. **Client:** TypeScript types regenerated (`openapi-typescript`) or manually updated and typecheck passes.
6. **Runtime:** One happy-path and one auth-failure path over real HTTP (compose or test client), not only mocks.

## Checklist

- [ ] Request schema matches implementation
- [ ] Response schema matches implementation
- [ ] Status codes documented and handled in UI
- [ ] Auth headers/cookies wired
- [ ] Permissions produce expected 401/403 UI
- [ ] Loading and error states use real failure modes
- [ ] Pagination keys match (`current`, `page_count`, `page_size`, `count`, `next`, `previous`, `results` if that is the project standard)

## Evidence

Paste command outputs and, if UI, confirm at least one live round-trip.

If contract tools are not installed, still: hit the endpoint with the project's test client and assert JSON shape the frontend expects. Do not skip.
