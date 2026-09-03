# Agent & Skill Formal Specifications (Catalog)

Detailed agent specs live under `agents/*/`. Skills live under `skills/**`. This catalog indexes them in the required schema.

## Agents

### Orchestrator

See `agents/orchestrator/OrchestratorSpec.md` (full schema).

### SecurityReviewer

See `agents/security-reviewer/SecurityReviewerSpec.md`.

### ArchitectureReviewer

See `agents/architecture-reviewer/ArchitectureReviewerSpec.md`.

---

## Skills (index)

Each skill file already contains: Name, Domain, Purpose, Trigger, Do Not Trigger, Procedure, Checks, Failures, Output, Related.

| Skill file | Name |
|------------|------|
| `skills/architecture/ArchitectureSkill.md` | architecture |
| `skills/backend/APIEngineerSkill.md` | api-engineer |
| `skills/backend/BackendQualitySkill.md` | backend-quality |
| `skills/backend/overlays/django-clean-architecture/DjangoCleanArchSkill.md` | django-clean-architecture |
| `skills/frontend/FrontendUIQualitySkill.md` | frontend-ui-quality |
| `skills/frontend/UIDesignQualitySkill.md` | ui-design-quality |
| `skills/frontend/AccessibilitySkill.md` | accessibility |
| `skills/database/MigrationReviewSkill.md` | migration-review |
| `skills/testing/TestStrategySkill.md` | test-strategy |
| `skills/testing/FlakyTestInvestigationSkill.md` | flaky-test-investigation |
| `skills/security/AppSecReviewSkill.md` | appsec-review |
| `skills/api/ContractIntegritySkill.md` | contract-integrity |
| `skills/devops/DockerSkill.md` | docker |
| `skills/devops/CICDSkill.md` | cicd |
| `skills/performance/PerformanceSkill.md` | performance |
| `skills/observability/ObservabilitySkill.md` | observability |
| `skills/git/GitHygieneSkill.md` | git-hygiene |
| `skills/review/CodeReviewSkill.md` | code-review |
| `skills/impact-analysis/ImpactAnalysisSkill.md` | impact-analysis |

## Cursor skill projections

`.cursor` copies under `adapters/cursor/skills/*/SKILL.md` point back to canonical workflows/skills for progressive disclosure in Cursor.
