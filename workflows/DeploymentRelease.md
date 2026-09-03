# Deployment / Release Workflow

Keep infrastructure as simple as the project profile allows. Do not require Kubernetes for an MVP.

## Flow

```
Confirm tests + lint on release candidate
    → Migrations ordered vs app deploy
    → Config/secrets present in target env
    → Health/readiness checks
    → Deploy
    → Smoke test
    → Rollback plan ready
```

## Checklist

- [ ] Image/build reproducible (lockfiles, pinned base images)
- [ ] Secrets not in image layers
- [ ] `HEALTHCHECK` or probe defined
- [ ] Rollback: previous image tag + reverse migration (or documented irreversible)
- [ ] Changelog / notes for operators if needed
- [ ] Zero/low downtime: expand/contract if schema change

## Docker Easy Path

Prefer `docker compose up` from `docker/fullstack/compose.yml` for local and small deploys.

## Skills

- `docker`
- `cicd`
- `observability` for production readiness
