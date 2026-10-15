# syntax=docker/dockerfile:1.10
# Django / DRF image. Build context = your project root:
#   docker build -f rigor-os/docker/django/Dockerfile .
# Uses uv when uv.lock exists, otherwise requirements.txt. Pin the base image by
# digest (python:3.14-slim@sha256:…) before shipping to production.
ARG PYTHON_VERSION=3.14

FROM python:${PYTHON_VERSION}-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev

COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /usr/local/bin/uv
WORKDIR /build
COPY pyproject.toml* uv.lock* requirements*.txt ./
RUN --mount=type=cache,target=/root/.cache \
    if [ -f uv.lock ]; then \
      uv sync --frozen --no-dev --no-install-project; \
    else \
      python -m venv /opt/venv && /opt/venv/bin/pip install -r requirements.txt; \
    fi

FROM python:${PYTHON_VERSION}-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=config.settings \
    GUNICORN_CMD_ARGS="--bind=0.0.0.0:8000 --workers=3 --timeout=60 --access-logfile=-"

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --shell /usr/sbin/nologin --no-create-home app

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app . .

# Opt in when static files are served from the image (e.g. WhiteNoise):
#   docker build --build-arg COLLECTSTATIC=1 …
# Fails the build on error instead of hiding it.
ARG COLLECTSTATIC=0
RUN if [ "$COLLECTSTATIC" = "1" ]; then SECRET_KEY=collectstatic-only python manage.py collectstatic --noinput; fi

USER app
EXPOSE 8000

# No curl in the image: the stdlib does the probe.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD ["python", "-c", "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health/', timeout=4).status < 500 else 1)"]

CMD ["gunicorn", "config.wsgi:application"]
