# Skill: CI/CD

```
Name: cicd
Domain: devops / supply chain
Purpose: Fast, repeatable, tamper-resistant pipelines without ceremony
Trigger: GitHub Actions/GitLab CI changes, release/deploy setup, dependency bots, "add CI", supply-chain hardening
Do Not Trigger: Local-only scripts unless asked
```

## Non-negotiables

1. **Same gates as local.** CI runs the commands in `project-context/COMMANDS.md` (or `tools/validate-gates.sh`) — no CI-only logic that developers cannot reproduce.
2. **Least-privilege tokens.** `permissions: {}` at workflow level; grant each job only what it needs (`contents: read`, `id-token: write` for OIDC, `packages: write` to publish).
3. **Pinned third-party actions** by full commit SHA with a `# vX.Y.Z` comment; a dependency bot (Dependabot `github-actions` ecosystem or Renovate `helpers:pinGitHubActionDigests`) keeps them current. Tag-pinning is how `tj-actions/changed-files` (Mar 2025) leaked secrets from thousands of repos.
4. **Audit workflows** with `zizmor` (template injection, `pull_request_target` misuse, credential persistence, cache poisoning).
5. **No long-lived cloud keys.** Deploy with OIDC federation (AWS/GCP/Azure/registries) and environment protection rules for production.
6. **Never `pull_request_target` + checkout of PR code** with secrets or write tokens. Keep untrusted builds and privileged publish in separate workflows.
7. **Provenance.** Build once, sign/attest (`actions/attest-build-provenance`, `gh attestation verify`), deploy the same digest everywhere; use immutable releases for published artifacts.

## Pipeline shape

```
PR:   lint/format → typecheck → unit → integration (service containers) → contract/OpenAPI diff
      → secret scan → dependency review → (frontend) build + Lighthouse budget → (SEO) seo_context --check
main: the above → build image (tag = git SHA) → SBOM + provenance attestation → push
deploy: environment-gated job consumes the digest; migrations run as a separate, reviewed step
```

## Speed

- `concurrency: { group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }` on PRs.
- Cache by lockfile: `astral-sh/setup-uv` (uv), `actions/setup-node` `cache: pnpm`, `Swatinem/rust-cache`, Docker `cache-from/to: type=gha`.
- Path filters / matrix only where it pays off; fail fast on lint before slow tests.
- `persist-credentials: false` on checkout unless the job pushes.

## Template

`templates/ci/github-actions-ci.yml` — Python (uv) + Node (pnpm) + Postgres service + secret scan + dependency review + zizmor, SHA-pinned. `templates/ci/dependabot.yml` for updates.

## Don't

- Require Kubernetes for a Compose-sized app
- Skip or `continue-on-error` tests to go green
- `curl | bash` installers in CI without checksum verification
- Store cloud keys as plain repository variables
- Reuse the PR build cache for release builds from forks

## Related

`docker`, `appsec-review`, `SecurityGate` (A03 Software Supply Chain Failures), `DeploymentRelease` workflow
