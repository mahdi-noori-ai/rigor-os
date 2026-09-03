# Security Gate

Aligned with [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/). Not every item applies to every change.

| ID | Risk | Verification |
|----|------|----------------|
| API1 | Broken Object Level Authorization | Test: user A cannot GET/PUT/DELETE user B's resource by ID |
| API2 | Broken Authentication | Tokens validated; login rate-limited; no tokens in URLs/logs |
| API3 | Broken Object Property Level Authorization | Serializer/DTO allow-lists; no mass assignment of privileged fields |
| API4 | Unrestricted Resource Consumption | Pagination limits; payload size; list endpoints not unbounded |
| API5 | Broken Function Level Authorization | Admin vs user endpoints; default deny |
| API6 | Unrestricted Access to Sensitive Business Flows | Abuse limits on signup, OTP, transfers |
| API7 | SSRF | User-supplied URLs allow-listed; no internal metadata IPs |
| API8 | Security Misconfiguration | CORS, cookies, DEBUG off in prod, error messages |
| API9 | Improper Inventory | New endpoints in OpenAPI; no shadow routes |
| API10 | Unsafe Consumption of APIs | Validate third-party responses; timeouts |

## Always (any new HTTP endpoint)

- [ ] Authentication requirement matches sibling endpoints
- [ ] Object-level permission on resource IDs
- [ ] Input validation at the boundary
- [ ] No secrets in code, logs, or client bundles

## Additional for Auth Changes

- [ ] Session/cookie flags (HttpOnly, Secure, SameSite) if cookies used
- [ ] Password/token reset flows not leaking account existence beyond project policy

## Additional for Uploads

- [ ] Type/size limits; stored outside web root or via signed URLs

## Tooling (prefer over prose)

- `bandit` / `pip-audit` / `npm audit` when dependencies change
- Secret scanners in hooks

Critical/high findings block DONE.
