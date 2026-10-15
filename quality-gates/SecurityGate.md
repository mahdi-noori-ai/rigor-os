# Security Gate

Aligned with [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/), [OWASP Top 10:2025](https://owasp.org/Top10/2025/), and — for AI features — the [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications/). Not every item applies to every change.

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

## Web application (OWASP Top 10:2025) — items not covered above

| ID | Risk | Verification |
|----|------|----------------|
| A02 | Security Misconfiguration | Secure headers, DEBUG off, default creds removed, least-privilege cloud/IAM |
| A03 | Software Supply Chain Failures | Lockfiles, dependency audit, SHA-pinned CI actions, SBOM/provenance for images |
| A04 | Cryptographic Failures | TLS everywhere incl. DB/proxy hops; no home-made crypto; secrets hashed/encrypted at rest |
| A09 | Security Logging & Alerting Failures | Auth failures and privilege changes logged and alertable; no secrets/PII in logs |
| A10 | Mishandling of Exceptional Conditions | Fail closed; generic error bodies; bounded retries/timeouts |

## AI / agent features (OWASP Agentic 2026, LLM 2025)

| ID | Risk | Verification |
|----|------|----------------|
| ASI01 | Agent goal hijack / prompt injection | Untrusted content (web, email, tickets, tool output) cannot trigger privileged tools without approval |
| ASI02 | Tool misuse | Tools least-privilege, argument schemas validated, destructive tools gated |
| ASI03 | Identity & privilege abuse | Agent acts with the user's scoped identity, not a shared admin key |
| ASI04 | Agentic supply chain | MCP servers/plugins pinned and reviewed (`MCPGovernanceSkill`) |
| ASI05 | Unexpected code execution | Model-generated code runs only in a sandbox |
| ASI06 | Memory & context poisoning | Persistent memory/RAG sources are attributed and writable only by trusted paths |
| — | Unbounded consumption | Token, cost, and rate limits per user |

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

- `bandit` / `pip-audit` / `pnpm audit` / `cargo audit` when dependencies change
- `gitleaks` or `trufflehog` (local + CI), `zizmor` for workflow changes
- Rigor guard hook (`adapters/hooks/guard_shell.py`) blocks destructive shell and `.env` printing

Critical/high findings block DONE.
