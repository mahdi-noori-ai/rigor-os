#!/usr/bin/env bash
# Run the deterministic quality gates that apply to this repository.
#
#   bash rigor-os/tools/validate-gates.sh [project_root] [--skip-tests]
#
# Exit code is non-zero when any gate that ran failed. A missing tool is a
# "skip", never a "pass" — the summary lists both so nobody mistakes one for
# the other (Constitution, Principle 2).
set -uo pipefail

OS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "$(basename "$OS")" == "rigor-os" ]]; then ROOT="$(dirname "$OS")"; else ROOT="$OS"; fi
SKIP_TESTS=0
for arg in "$@"; do
  case "$arg" in
    --skip-tests) SKIP_TESTS=1 ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) ROOT="$(cd "$arg" && pwd)" ;;
  esac
done
cd "$ROOT" || exit 2
export CI="${CI:-true}"

PASSED=() FAILED=() SKIPPED=()

gate() { # gate NAME CMD...
  local name="$1"; shift
  echo "==> $name: $*"
  if "$@"; then PASSED+=("$name"); else FAILED+=("$name (exit $?)"); fi
}
skip() { echo "--  skip $1: $2"; SKIPPED+=("$1 ($2)"); }
has() { command -v "$1" >/dev/null 2>&1; }

# ---- Python
if [[ -f pyproject.toml || -f requirements.txt ]]; then
  PY=()
  if [[ -f uv.lock ]] && has uv; then PY=(uv run --frozen); elif [[ -f poetry.lock ]] && has poetry; then PY=(poetry run); fi
  if "${PY[@]}" ruff --version >/dev/null 2>&1; then
    gate "ruff check" "${PY[@]}" ruff check .
    gate "ruff format" "${PY[@]}" ruff format --check .
  else skip ruff "not installed"; fi
  if [[ $SKIP_TESTS -eq 0 ]]; then
    if "${PY[@]}" python -c "import pytest" >/dev/null 2>&1; then
      echo "==> pytest"
      "${PY[@]}" python -m pytest -q; rc=$?
      if [[ $rc -eq 0 ]]; then PASSED+=("pytest"); elif [[ $rc -eq 5 ]]; then skip pytest "no tests collected"; else FAILED+=("pytest (exit $rc)"); fi
    else skip pytest "not installed"; fi
  fi
fi

# ---- JavaScript / TypeScript (never installs anything)
if [[ -f package.json ]]; then
  if [[ -f pnpm-lock.yaml ]]; then PM=pnpm; elif [[ -f yarn.lock ]]; then PM=yarn; elif [[ -f bun.lock || -f bun.lockb ]]; then PM=bun; else PM=npm; fi
  if [[ ! -d node_modules ]]; then
    skip "$PM scripts" "node_modules missing — install dependencies first"
  elif has "$PM"; then
    has_script() { python3 -c "import json,sys; sys.exit(0 if '$1' in json.load(open('package.json')).get('scripts',{}) else 1)"; }
    has_script lint && gate "$PM lint" "$PM" run lint
    if has_script typecheck; then gate "$PM typecheck" "$PM" run typecheck
    elif [[ -x node_modules/.bin/tsc && -f tsconfig.json ]]; then gate "tsc" node_modules/.bin/tsc --noEmit
    fi
    [[ $SKIP_TESTS -eq 0 ]] && has_script test && gate "$PM test" "$PM" run test
  else skip "$PM" "not installed"; fi
fi

# ---- Rust / Go
if [[ -f Cargo.toml ]]; then
  if has cargo; then
    gate "cargo fmt" cargo fmt --all --check
    gate "cargo clippy" cargo clippy --workspace --all-targets -- -D warnings
    [[ $SKIP_TESTS -eq 0 ]] && gate "cargo test" cargo test --workspace
  else skip cargo "not installed"; fi
fi
if [[ -f go.mod ]]; then
  if has go; then
    gate "go vet" go vet ./...
    [[ $SKIP_TESTS -eq 0 ]] && gate "go test" go test ./...
  else skip go "not installed"; fi
fi

# ---- Secrets
if has gitleaks; then gate "gitleaks" gitleaks git --no-banner --redact .
elif has trufflehog; then gate "trufflehog" trufflehog git "file://$ROOT" --only-verified --fail --no-update
else skip "secret scan" "install gitleaks or trufflehog"; fi

# ---- SEO (only when the repo has a public web surface)
if has python3 && python3 "$OS/tools/bootstrap.py" --root "$ROOT" --json 2>/dev/null | python3 -c "import json,sys; sys.exit(0 if json.load(sys.stdin)['seo_surface'] else 1)"; then
  gate "seo metadata" python3 "$OS/tools/seo_context.py" --root "$ROOT" --stdout --check >/dev/null
fi

echo
echo "passed : ${#PASSED[@]} ${PASSED[*]:+— ${PASSED[*]}}"
echo "skipped: ${#SKIPPED[@]}"; for s in "${SKIPPED[@]:-}"; do [[ -n "$s" ]] && echo "   - $s"; done
echo "failed : ${#FAILED[@]}"; for f in "${FAILED[@]:-}"; do [[ -n "$f" ]] && echo "   - $f"; done
[[ ${#FAILED[@]} -eq 0 ]]
