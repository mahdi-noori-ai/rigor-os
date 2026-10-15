# Model Routing (per project)

Map Rigor logical tiers to **your** tool’s model IDs.  
Agents read this file; they must not invent spendier models than configured.

## Policy

- Low tasks → `economy` / `standard`
- Orchestrator planning (Medium+) + Security/Architecture reviewers → `max`
- See `standards/ModelRoutingMatrix.md`

## Aliases (edit me)

| Alias | Cursor | Claude Code (model · effort) | Codex / other | Notes |
|-------|--------|------------------------------|---------------|-------|
| economy | _e.g. fast/composer-small_ | _haiku · low_ | _default-fast · low_ | T0 |
| standard | _default agent_ | _sonnet · medium_ | _default · medium_ | T1 |
| strong | _strong agent_ | _sonnet · high_ | _default · high_ | T2 |
| max | _best / thinking_ | _opus · xhigh_ | _best · high_ | T3 leads & reviewers |

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
| SEO Strategist (route specs) | strong |
| SEO Strategist (launch / positioning / multi-locale) | max |

## Session notes

_Optional: last routing decisions, cost incidents, preferred defaults._
