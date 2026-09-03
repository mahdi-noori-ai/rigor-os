# Safe Autonomy

Boundaries for autonomous AI agent behavior. Enforce via hooks where possible; treat as non-negotiable rules otherwise.

## Forbidden Without Explicit Approval

| Action | Why | Enforcement |
|--------|-----|-------------|
| `rm -rf /` or recursive delete of system paths | Irreversible data loss | Hook: `beforeShellExecution` deny |
| `DROP DATABASE`, `TRUNCATE`, production DDL | Data destruction | Hook deny + rule |
| `git push --force` to main/master | History destruction | Hook deny |
| Commit secrets, API keys, tokens | Security breach | Hook scan + rule |
| Modify production environment | Blast radius | Hook deny production URLs |
| Disable/skip failing tests | False confidence | Rule + TestingGate |
| Suppress lint/type errors | Hidden defects | Rule |
| Install new dependencies without justification | Supply chain risk | Rule + ask user |

## Required Before Editing

1. **Read** the files you will modify.
2. **Understand** the existing pattern in that area.
3. **Identify** affected domains (backend, frontend, DB, tests, docs).
4. **Plan** the smallest change that satisfies the requirement.

## Required Before Declaring Complete

1. Run lint on changed files.
2. Run relevant tests.
3. Verify integration if API or UI changed.
4. Check diff for unrelated changes.

## Permission Boundaries for Tools/MCP

- Grant only tools required for the current task.
- Database write access: ask first.
- External API calls: ask first unless documented in project context.
- Browser automation: scoped to localhost/staging unless approved.

## Escalation

When an action is blocked or uncertain:
- Explain what you want to do and why.
- Present options with trade-offs.
- Wait for user decision.
- Never bypass safety by rephrasing the same dangerous command.

## Retry Policy

| Attempt | Action |
|---------|--------|
| 1 | Implement + verify |
| 2 | Diagnose failure, fix root cause |
| 3 | Try alternative approach |
| After 3 | Report BLOCKED with evidence |

Do not loop indefinitely. Do not declare success on partial completion.
