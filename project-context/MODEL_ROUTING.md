# Model Routing (per project)

Map Rigor logical tiers to **your** tool’s model IDs.  
Agents read this file; they must not invent spendier models than configured.

## Policy

- Low tasks → `economy` / `standard`
- Orchestrator planning (Medium+) + Security/Architecture reviewers → `max`
- See `standards/ModelRoutingMatrix.md`

## Aliases (edit me)

| Alias | Cursor | Claude Code | Codex / other | Notes |
|-------|--------|-------------|---------------|-------|
| economy | _e.g. fast/composer-small_ | _e.g. haiku_ | _default-fast_ | T0 |
| standard | _default agent_ | _sonnet_ | _default_ | T1 |
| strong | _strong agent_ | _sonnet_ | _default_ | T2 |
| max | _best / thinking_ | _opus / best_ | _best_ | T3 leads & reviewers |

If a cell is empty, use the next lower alias that is set; if only `max` exists, still enforce **context budgets** by tier.

## Role binding

| Role | Alias |
|------|-------|
| Implementer T0 | economy |
| Implementer T1 | standard |
| Implementer T2 | strong |
| Orchestrator plan Medium+ | max |
| Security Reviewer | max |
| Architecture Reviewer | max |

## Session notes

_Optional: last routing decisions, cost incidents, preferred defaults._
