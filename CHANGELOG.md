# Changelog

## 1.1.0 — 2026-10-15 (optimized fork)

Fork of [sajadfallahdoost/rigor-os](https://github.com/sajadfallahdoost/rigor-os) at `ca638be`. The architecture
(constitution → skills → workflows → gates → adapters, three core agents) is unchanged. What changed and why:

### Added
- **SEO agent.** `agents/seo-strategist/`, `skills/seo/SEOContextSkill.md`, `workflows/SEOContextGeneration.md`,
  `quality-gates/SEOGate.md`, `templates/SEOContext.md`, `templates/llms.txt`, Cursor rule `seo.mdc`, Claude and
  Copilot agent definitions, and `tools/seo_context.py` — a stdlib, offline extractor for Next.js (app + pages),
  Astro, SvelteKit, Nuxt, Remix, HTML/Vite, Django/Jinja, and Markdown. `--check` is a CI gate.
- **MCP governance** skill and pinned `templates/mcp.json.example` (MCP spec 2026-07-28, OWASP Agentic Top 10).
- **PostgreSQL scaling** skill; PgBouncer compose profile; `docker/shahrah/` overlay for region-aware sharding with
  [shahrah](https://github.com/mahdi-noori-ai/shahrah).
- **CI/CD templates** (`templates/ci/`): SHA-pinned actions, `permissions: {}`, zizmor, gitleaks, dependency review,
  SBOM + provenance attestation, Dependabot.
- Portable skills `seo-context`, `mcp-governance`, `postgres-scaling`, `ci-cd`.
- Copilot custom agents (`adapters/copilot/agents/*.agent.md`).
- Repository CI (`.github/workflows/ci.yml`), Dependabot, `pyproject.toml` (ruff/pytest), `tests/` (54 tests),
  `tools/check_links.py`.
- Constitution Principle 9: untrusted input (web, tool, MCP output) is data.

### Fixed
- `adapters/codex/hooks.json` used a top-level `{"PreToolUse": …}`; Codex requires `{"hooks": {…}}`, so the guard
  never loaded.
- Cursor `deny-destructive.sh` returned `allow` whenever `jq` was missing.
- Claude hook printed the legacy `{"decision": "block"}`; now `hookSpecificOutput.permissionDecision: "deny"`.
- Destructive-command regexes missed `rm -fr /`, `rm -r -f ~`, `sudo rm …`, `bash -c '…'`, `git push -f`, `+main`.
- `tools/bootstrap.py` overwrote `PROJECT_CONTEXT.md` (and the rest) on every run, destroying user edits; it also
  globbed through `node_modules`/`.venv`.
- `tools/validate-gates.sh` ran `pytest || true` and `npm run lint || true`, reporting failures as success, and
  `npx --yes tsc` installed packages without asking.
- `tools/sync-adapters.sh` only worked when vendored as `rigor-os/` (README claimed both layouts); `all` overwrote
  `AGENTS.md` twice; replaced files were lost silently (now `*.bak`).
- `docker/django/compose.yml` and `docker/react/compose.yml` pointed at a nested rigor-os/rigor-os/ Dockerfile path (wrong build context)
  and an .env inside rigor-os/.
- `collectstatic … || true` hid build failures; `SECRET_KEY` defaulted to `change-me-in-env`; DB/Redis ports were
  published on all interfaces.

### Changed
- Skills moved from `adapters/cursor/skills/` to `adapters/skills/` (Agent Skills standard) and are installed for every
  tool: `.cursor/skills`, `.claude/skills`, `.agents/skills` (Codex), `.github/skills` (Copilot).
- Reviewer subagents: `model: opus`, `effort`, `permissionMode: plan`, `disallowedTools` (actually read-only).
- Claude permissions: deny secret files (keeps `.env.example` readable), ask before push/dependency installs.
- Docker: Postgres 18 (volume at `/var/lib/postgresql`), `pg_stat_statements`, Python 3.14 + uv, Node 24,
  Redis 8 (Valkey noted), `nginx-unprivileged`, BuildKit cache mounts, security headers, gzip, stdlib healthchecks.
- `SecurityGate`/`AppSecReviewSkill`: OWASP Top 10:2025 (supply chain, exceptional conditions) and Agentic 2026.
- `ModelRoutingMatrix`: reasoning effort as a routing dial; prompt-cache guidance.
- `DefaultStackMatrix`, `CICDSkill`, `DockerSkill`, `PerformanceSkill` (Core Web Vitals), orchestrator skill table,
  quality-gate matrix (SEOGate, supply chain), taxonomy (opt-in fourth agent).
