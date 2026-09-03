# Skill: Docker

```
Name: docker
Domain: devops
Purpose: Easy, secure, reproducible containers
Trigger: Dockerfiles, compose, local bring-up, image size/security
Do Not Trigger: Application logic with no container change
```

## Non-negotiables

1. Multi-stage builds (builder vs runtime).
2. Non-root user in runtime.
3. `.dockerignore` (no `.git`, `.env`, node_modules, venv).
4. Healthcheck.
5. Secrets via env/files, not baked in.
6. Pin base image tags (digest when going to prod).
7. Dev vs prod compose overlay — don't run `runserver` in prod images.

## Easy bring-up goal

A new engineer (or agent) should run:

```bash
cp .env.example .env
docker compose -f docker/fullstack/compose.yml up --build
```

and get API + web + postgres + redis healthy.

## Django notes

- `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`
- gunicorn/uvicorn in prod stage
- `libpq5` in runtime, build tools only in builder
- collectstatic in build when serving static from image or volume strategy documented

## React notes

- Node stage builds assets; nginx (or similar) serves
- SPA fallback to `index.html`
- Cache hashed assets; no-cache `index.html`
