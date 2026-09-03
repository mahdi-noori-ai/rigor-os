# Research Report — AI Software Engineering Operating System

Language note: architectural conclusions below are in English for portability of the framework documents. Sources are English-language primary docs.

## 1. Current state of agentic coding configuration

### Cursor

- **Project Rules**: `.cursor/rules/*.mdc` with frontmatter `description`, `globs`, `alwaysApply`. Plain `.md` in rules is ignored. Nested rules possible. ([Cursor Rules docs](https://cursor.com/docs/rules))
- **AGENTS.md**: portable plain Markdown; root + nested. Good cross-tool kernel.
- **Skills**: folders with `SKILL.md`; `description` drives relevance; optional `scripts/`, `references/`, `assets/`. `/migrate-to-skills` converts eligible dynamic rules. ([Cursor Skills](https://cursor.com/docs/skills))
- **Hooks**: `.cursor/hooks.json` stdio JSON; events include `beforeShellExecution`, `afterFileEdit`, `preToolUse`, `stop`. Can allow/ask/deny shell. ([Cursor Hooks](https://cursor.com/docs/hooks))

### Claude Code

- **CLAUDE.md**: always-on project kernel.
- **Skills**: `SKILL.md` with auto-invocation via description; progressive loading.
- **Subagents**: isolated context, tool allowlists; good for review roles.
- **Hooks**: `PreToolUse` can block even under bypass modes; deterministic enforcement preferred for safety. ([Hooks reference](https://code.claude.com/docs/en/hooks), [Permissions](https://code.claude.com/docs/en/permissions))
- **MCP**: external tools; least privilege recommended.

### OpenAI Codex

- **AGENTS.md** discovery: global → project root → path to cwd; closer wins; default **32 KiB** combined budget — large roots starve nested files. ([Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md), [agents.md](https://agents.md/))
- **Hooks / config.toml**: lifecycle hooks and MCP permission filtering. ([Codex hooks](https://developers.openai.com/codex/hooks))

### GitHub Copilot

- `.github/copilot-instructions.md` repo-wide.
- `.github/instructions/*.instructions.md` with `applyTo` globs (path-specific).
- Also reads `AGENTS.md` / `CLAUDE.md` on some surfaces. ([GitHub docs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions))

## 2. Patterns observed

1. **Progressive disclosure**: always-on kernels stay small; procedures live in skills.
2. **Deterministic hooks** beat prompt-only safety.
3. **Cross-tool AGENTS.md** is the emerging portable standard.
4. **Agent explosion** is a common failure mode in community multi-agent setups; manager-worker helps coordination but costs tokens and loses context at handoffs. ([Manager-worker](https://oracle.github.io/agent-spec/26.1.0/howtoguides/howto_managerworkers.html), [Governed autonomy](https://www.agent-engineering.ch/articles/governed-autonomy-supervisor-worker-skill-graphs/))
5. **Contract as artifact**: OpenAPI + lint + breaking-change diff + live schema tests. ([OpenAPI contract testing guidance](https://qaskills.sh/blog/openapi-3-1-contract-testing-guide-2026))
6. **Test pyramid**: favor small/fast tests; manage flakes via hermeticity. ([Software Engineering at Google — Testing](https://abseil.io/resources/swe-book/html/ch11.html))
7. **OWASP API Top 10 2023**: authorization still dominates. ([OWASP](https://owasp.org/API-Security/editions/2023/en/0x11-t10/))
8. **Docker**: multi-stage, non-root, healthchecks for production-minded images.

## 3. Strongest approaches

- Hybrid: **one implementer session + skills + gates + rare read-only reviewers**
- Canonical folder + thin adapters
- Project memory that stores *commands and boundaries*, not duplicated source
- UI quality as a first-class skill (human preference, high vibe-coding failure rate)

## 4. Conflicting approaches

| Conflict | Resolution |
|----------|------------|
| Deep hierarchy vs flat rules | Prefer hybrid; hierarchy only for security/arch review |
| Everything in CLAUDE.md vs skills | Keep kernel tiny |
| Generated adapters vs symlinks | Prefer copy/sync script (works on all OS; no symlink pain on Windows) |
| Schema-first vs code-first | Prefer project's existing culture; if schemas co-located with views, keep that |

## 5. Answers to required research questions (summary)

1. **Always load:** constitution, safety, project-context summary, skill *descriptions*.
2. **Conditional:** full skills, workflows, templates, reviewer agents.
3. **Rules:** non-negotiables and path constraints.
4. **Skills:** procedures and domain expertise.
5. **Autonomous agent:** implementer (orchestrator session); reviewers for independence.
6. **Deterministic tooling:** lint, types, tests, schema, secret scan, hooks.
7. **May modify code:** Orchestrator/implementer only.
8. **Read-only:** Security + Architecture reviewers.
9. **Cross-domain:** impact-analysis + API change workflow + integration gate.
10. **Contract integrity:** OpenAPI + consumer types + live verification.
11. **Finished:** contextual DoD + evidence.
12. **Retries:** max 3 then BLOCKED.
13. **Conflicts:** single writer; reviewers advise, orchestrator applies.
14. **Persistence:** project-context + ADRs.
15. **Portability:** canonical `rigor-os/` + adapters.
16. **Token minimize:** progressive disclosure; lean AGENTS.md.
17. **Avoid too many agents:** three roles max.
18. **Avoid doc bloat:** evolution process; prefer tests.
19. **Avoid overengineering:** YAGNI + size profiles.
20. **Evolve:** mistake → tool > rule > skill > doc.

## 6. Architecture options (evaluated)

- **A Flat rules+skills** — weak integration.
- **B Deep hierarchy** — costly handoffs.
- **C Hybrid orchestrator + skills + deterministic gates** — **chosen**.

## 7. Fact vs recommendation

| Fact | Recommendation |
|------|----------------|
| Tools load AGENTS.md / rules / skills differently | Keep canonical source; generate adapters |
| Hooks can deny shell | Put destructive patterns in hooks |
| Codex truncates AGENTS.md | Keep Codex AGENTS lean |
| OWASP lists authorization risks | SecurityGate + tests for BOLA |

## Citations (selected)

- https://cursor.com/docs/rules
- https://cursor.com/docs/skills
- https://cursor.com/docs/hooks
- https://code.claude.com/docs/en/skills.md
- https://code.claude.com/docs/en/hooks
- https://developers.openai.com/codex/guides/agents-md
- https://agents.md/
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions
- https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- https://abseil.io/resources/swe-book/html/ch11.html
- https://opentelemetry.io/docs/specs/otel/logs/data-model/
