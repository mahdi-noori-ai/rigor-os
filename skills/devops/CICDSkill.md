# Skill: CI/CD

```
Name: cicd
Domain: devops
Purpose: Repeatable pipelines without ceremony
Trigger: GitHub Actions/GitLab CI, release, environment config
Do Not Trigger: Local-only scripts unless asked
```

## Procedure

1. Lint, typecheck, unit tests on PR.
2. Integration tests when DB needed (service containers).
3. Secret scanning.
4. Build image on main; tag with git sha.
5. Deploy job separate from test job; production needs approval if possible.

## Don't

- Require K8s for a Compose-sized app
- Skip tests to go green
- Store cloud keys in repo variables unencrypted
