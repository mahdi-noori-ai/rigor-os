# Failure Scenarios → Framework Catch

| Failure | Catch |
|---------|-------|
| API changed; frontend not updated | `APIChange` workflow + `contract-integrity` + IntegrationVerification (DoD blocks without FE sync) |
| Migration OK locally, unsafe in prod | `migration-review` + DatabaseMigration workflow (expand/contract, locks) |
| Page works on desktop only | `frontend-ui-quality` + FrontendUIFeature + DoD responsive checks |
| Agent comments out failing test | TestingGate forbidden + constitution + safety rule |
| Vulnerable dependency added | SecurityGate tooling (`pip-audit`/`npm audit`) + AppSec skill |
| N+1 queries introduced | Performance skill + Architecture/DoD performance when hot path |
| Two agents incompatible assumptions | Architecture C: single implementer session; no parallel writers |
| AI rewrites unrelated code | Constitution "smallest correct diff" + ArchitectureGate |
| Feature works but lacks authorization | SecuritySensitive workflow + SecurityGate API1/API5 + SecurityReviewer |
| Claims success without tests | DoD evidence requirement + Orchestrator completion criteria |
| Fat view with ORM | `django-clean-architecture` + ArchitectureGate |
| Robotic ugly UI | `ui-design-quality` skill |
| Skipped Ruff | python-backend rule + BackendQuality |
| Infinite verify loop | SafeAutonomy 3-attempt → BLOCKED |
| Secrets in commit | safety rule + hooks |
| New `{success,data}` envelope | API engineer + Django overlay response style |
| Client-trusted game currency/score | `mobile-game` + `mobile-backend-api` + MobileGate |
| Android UI happy-path only | `mobile-ui-ux` + MobileGate offline/error |
| API DTO drift on Kotlin client | `mobile-api-client` + contract-integrity |
| IAP grant without Play verify | `mobile-backend-api` + `mobile-security` |
| “Works in Unity Editor” only | MobileGate device/Android build smoke |
| Keystore committed | `mobile-release` + safety rules |
