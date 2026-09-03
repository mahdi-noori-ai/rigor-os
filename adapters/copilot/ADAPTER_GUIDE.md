# GitHub Copilot Adapter Guide

| Canonical | Copilot |
|-----------|---------|
| Repo-wide | `.github/copilot-instructions.md` |
| Path-specific | `.github/instructions/*.instructions.md` with `applyTo` globs |
| Cross-tool | Root `AGENTS.md` (also used by other agents) |

Not all Copilot surfaces support every instruction type equally — see GitHub docs for cloud agent vs IDE. Keep deep procedures in `rigor-os/` and summarize here.

Install: `bash rigor-os/tools/sync-adapters.sh copilot`
