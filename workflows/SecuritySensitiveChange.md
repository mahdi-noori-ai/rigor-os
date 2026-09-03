# Security-Sensitive Change Workflow

Use when touching authentication, authorization, sessions, tokens, PII, file uploads, payments, or secrets.

## Mandatory

1. Load `AppSecReviewSkill` and `SecurityGate`.
2. Invoke Security Reviewer agent after implementation (read-only).
3. Tests must cover unauthorized access (403/401) and object-level checks (user A cannot access user B's resource).
4. Never log tokens, passwords, full PII.
5. Rate-limit auth endpoints if adding login/OTP.

## Flow

```
Threat sketch (who can abuse this?)
    → Implement with deny-by-default authz
    → Tests for BOLA / function-level auth
    → SecurityGate checklist
    → Security Reviewer
    → Fix findings
    → Deliver
```

## OWASP API Focus (minimum)

- API1 Broken Object Level Authorization
- API2 Broken Authentication
- API3 Broken Object Property Level Authorization (mass assignment)
- API5 Broken Function Level Authorization
- Secrets/config (API8)

Do not ship "it works when I call it as admin" as proof of security.
