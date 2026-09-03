# Skill: AppSec Review

```
Name: appsec-review
Domain: security
Purpose: Adversarial review mapped to OWASP API Top 10 2023
Trigger: Auth, permissions, user data, uploads, new endpoints, secrets, SSRF-ish URL fetchers
Do Not Trigger: Isolated styling
```

## Procedure

1. List new/changed endpoints and who may call them.
2. For each resource ID from the client: verify ownership/authorization in server code (not only UI hiding).
3. Serializer extra_kwargs / read-only fields — privileged properties not writable.
4. Injection: ORM parameterization; no raw SQL from user input; no HTML unsanitized if you render it.
5. SSRF: user URLs.
6. Secrets: env only; never in git.
7. CORS: explicit origins in prod.
8. Tests: 401 unauthenticated, 403 other user.

## Common failures

- ID in URL trusted
- Admin flag in PATCH body
- JWT `alg=none` or skipping verification
- Logging Authorization headers
