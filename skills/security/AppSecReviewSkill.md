# Skill: AppSec Review

```
Name: appsec-review
Domain: security
Purpose: Adversarial review mapped to OWASP Top 10:2025, API Security Top 10 (2023), LLM Top 10 (2025) and Agentic Top 10 (2026)
Trigger: Auth, permissions, user data, uploads, new endpoints, secrets, SSRF-ish URL fetchers, dependency changes, LLM features, agent tools / MCP servers
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
9. Supply chain (A03:2025): new dependency justified, lockfile committed, `pip-audit` / `pnpm audit` / `cargo audit` clean, no typosquats, CI actions SHA-pinned.
10. Errors (A10:2025 Mishandling of Exceptional Conditions): fail closed on auth/permission errors; no stack traces or SQL in responses; timeouts and retries bounded.
11. LLM / agent features: treat model output and tool results as untrusted input (prompt injection), constrain tools to least privilege, require human approval for irreversible actions, never put secrets in prompts, rate-limit and cap tokens (unbounded consumption). MCP changes → `skills/ai/MCPGovernanceSkill.md`.

## Common failures

- ID in URL trusted
- Admin flag in PATCH body
- JWT `alg=none` or skipping verification
- Logging Authorization headers
- Rendering LLM output as HTML/Markdown links without sanitising (exfiltration via image URLs)
- An agent tool that can both read private data and send it to an arbitrary URL
