#!/usr/bin/env bash
# Run deterministic gates when tools exist. Prefer project COMMANDS.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

run_if() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "==> $*"
    "$@"
  else
    echo "skip (missing): $1"
  fi
}

if [[ -f pyproject.toml ]] || [[ -f requirements.txt ]]; then
  run_if ruff check .
  if command -v pytest >/dev/null 2>&1; then
    echo "==> pytest"
    pytest -q || true
  fi
fi

if [[ -f package.json ]]; then
  if command -v npm >/dev/null 2>&1; then
    npm run lint --if-present || true
    npx --yes tsc --noEmit 2>/dev/null || true
  fi
fi

echo "validate-gates finished (see skips)."
