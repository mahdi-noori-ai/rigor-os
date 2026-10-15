---
name: ci-cd
description: Create or harden CI/CD pipelines — GitHub Actions with SHA-pinned actions, least-privilege permissions, zizmor, Dependabot, secret scanning, OIDC deploys, SBOM and provenance attestations. Use when adding or changing workflows, release, or deployment automation.
---

# CI/CD

Follow `${CLAUDE_PLUGIN_ROOT}/skills/devops/CICDSkill.md`; start from `${CLAUDE_PLUGIN_ROOT}/templates/ci/github-actions-ci.yml` and `${CLAUDE_PLUGIN_ROOT}/templates/ci/dependabot.yml`.

CI runs the same commands as `project-context/COMMANDS.md`. `permissions: {}` by default, pin actions by SHA, run `zizmor` on workflow changes.
