# Quality Gate Matrix

**M** = mandatory · **O** = optional / when relevant · **—** = skip

| Gate | Tiny UI | Bug fix | Backend service | API change | FE+BE feature | Migration | Auth/security | Perf work | Release | Docs only |
|------|---------|---------|-----------------|------------|---------------|-----------|---------------|-----------|---------|-----------|
| Lint / format | M | M | M | M | M | M | M | M | M | O |
| Typecheck | O | O | O | M | M | — | O | O | M | — |
| Unit tests | — | M | M | M | M | O | M | O | M | — |
| Integration tests | — | O | O | M | M | M | M | O | M | — |
| Contract / OpenAPI | — | — | O | M | M | — | O | — | M | — |
| E2E | — | — | — | O | O | — | O | — | O | — |
| SecurityGate | — | O | O | O | O | — | M | — | O | — |
| ArchitectureGate | — | — | M | M | M | O | M | — | — | — |
| IntegrationVerification | — | — | — | M | M | — | O | — | O | — |
| Migration review | — | — | — | — | O | M | — | — | O | — |
| Responsive UI | M | O | — | — | M | — | — | O | O | — |
| Accessibility | O | — | — | — | M | — | — | — | O | — |
| Performance | — | — | O | — | O | O | — | M | O | — |
| Observability | — | O | O | O | O | — | O | O | O | — |
| Documentation | — | O | O | M | O | O | O | — | M | M |
| Deployment impact | — | — | — | O | O | M | O | — | M | — |

Profile **Small** may downgrade E2E and Observability to —. Profile **Large** upgrades E2E to M for user-facing features.
