# Quality Gate Matrix

**M** = mandatory · **O** = optional / when relevant · **—** = skip

| Gate | Tiny UI | Bug fix | Backend service | API change | FE+BE feature | Migration | Auth/security | Perf work | Release | Docs only | Android feature | Mobile game feature | Android release |
|------|---------|---------|-----------------|------------|---------------|-----------|---------------|-----------|---------|-----------|-----------------|---------------------|-----------------|
| Lint / format | M | M | M | M | M | M | M | M | M | O | M | M | M |
| Typecheck | O | O | O | M | M | — | O | O | M | — | O | O | O |
| Unit tests | — | M | M | M | M | O | M | O | M | — | M | M | O |
| Integration tests | — | O | O | M | M | M | M | O | M | — | O | O | O |
| Contract / OpenAPI | — | — | O | M | M | — | O | — | M | — | O | O | — |
| E2E / device smoke | — | — | — | O | O | — | O | — | O | — | M | M | M |
| SecurityGate | — | O | O | O | O | — | M | — | O | — | O | O | O |
| ArchitectureGate | — | — | M | M | M | O | M | — | — | — | M | M | — |
| IntegrationVerification | — | — | — | M | M | — | O | — | O | — | M* | M* | — |
| Migration review | — | — | — | — | O | M | — | — | O | — | — | — | — |
| Responsive / touch UI | M | O | — | — | M | — | — | O | O | — | M | M | O |
| Accessibility | O | — | — | — | M | — | — | — | O | — | O | — | — |
| Performance | — | — | O | — | O | O | — | M | O | — | O | O | O |
| Observability | — | O | O | O | O | — | O | O | O | — | O | O | O |
| Documentation | — | O | O | M | O | O | O | — | M | M | O | O | M |
| Deployment impact | — | — | — | O | O | M | O | — | M | — | — | — | M |
| **MobileGate** | — | O | — | O | — | — | O | — | O | — | **M** | **M** | **M** |
| **SEOGate**† | O | — | — | — | M† | — | — | O | M† | O | — | — | O‡ |
| Supply chain (deps/CI pinning) | — | O | O | O | O | — | M | — | M | — | O | O | M |

\* When the change includes backend ↔ client API.
† Only for public, indexable web routes (skip auth-only/internal apps). ‡ Store-listing ASO for Play releases.

Profile **Small** may downgrade instrumented E2E to device smoke only. Profile **Large** upgrades instrumented tests to M for critical mobile flows.
