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
6. Pin base image tags (digest when going to prod); let Dependabot/Renovate bump them.
7. Dev vs prod compose overlay — don't run `runserver` in prod images.
8. BuildKit cache mounts for package managers (`--mount=type=cache`) instead of bloated layers.
9. Bind dev-only ports to `127.0.0.1`; required secrets fail fast (`${SECRET_KEY:?…}`), never default to a placeholder.
10. Build failures stay failures — no `|| true` around `collectstatic`, migrations, or builds.

## Easy bring-up goal

A new engineer (or agent) should run:

```bash
cp rigor-os/docker/fullstack/.env.example .env   # set SECRET_KEY
docker compose -f rigor-os/docker/fullstack/compose.yml --env-file .env up --build
```

and get API + web + postgres + redis healthy. Overlays: `--profile pooler` (PgBouncer), `docker/shahrah/` (region-aware sharding proxy).

## Current defaults (Oct 2026)

| Component | Image | Note |
|-----------|-------|------|
| Python | `python:3.14-slim` | 3.15.0 shipped 2026-10-09 — move once your wheels support it |
| Node | `node:24-alpine` | LTS; Node 26 becomes the next LTS line |
| PostgreSQL | `postgres:18-alpine` | **Mount the volume at `/var/lib/postgresql`** (18 stores data in `18/docker`) |
| Redis | `redis:8-alpine` | or `valkey/valkey:9-alpine` (BSD licence) |
| Nginx | `nginxinc/nginx-unprivileged:1.28-alpine` | runs as non-root on 8080 |
| uv | `ghcr.io/astral-sh/uv:0.9` | copy the binary into the builder stage |

## Django notes

- `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`
- gunicorn/uvicorn in prod stage
- `libpq5` in runtime, build tools only in builder
- `uv sync --frozen --no-dev` when `uv.lock` exists; `requirements.txt` otherwise
- collectstatic in build only when static files are served from the image (`--build-arg COLLECTSTATIC=1`)
- Healthcheck with the stdlib (`urllib`) — no curl in the runtime image

## React notes

- Node stage builds assets; nginx (or similar) serves
- SPA fallback to `index.html` — but never for `robots.txt`, `sitemap.xml`, `llms.txt`
- Cache hashed assets; no-cache `index.html`
- Next.js SSR: `output: "standalone"` and a Node runtime stage instead of nginx
