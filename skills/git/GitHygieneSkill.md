# Skill: Git Hygiene

```
Name: git-hygiene
Domain: git
Purpose: Reviewable, atomic changes
Trigger: Commits, PRs, lockfiles, generated files
```

## Rules

- Atomic commits when the user wants commits
- Don't reformat the universe
- Don't commit `.env`, secrets, `tmp/`
- Summarize PR: why, what, test evidence
- Lockfiles committed when the project already commits them
- Don't force-push shared main
