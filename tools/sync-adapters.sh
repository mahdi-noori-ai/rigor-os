#!/usr/bin/env bash
# Project Rigor OS adapters into a host repository.
#
#   bash rigor-os/tools/sync-adapters.sh {cursor|claude|codex|copilot|all} [target_root] [--dry-run]
#
# Works both when Rigor OS is vendored as ./rigor-os and when its contents sit at
# the repository root. Existing files that differ are backed up to *.bak first.
set -euo pipefail

OS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "$(basename "$OS")" == "rigor-os" ]]; then
  DEFAULT_TARGET="$(dirname "$OS")"
else
  DEFAULT_TARGET="$OS"
fi

ADAPTER=""
TARGET=""
DRY=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) if [[ -z "$ADAPTER" ]]; then ADAPTER="$arg"; else TARGET="$arg"; fi ;;
  esac
done
ADAPTER="${ADAPTER:-cursor}"
TARGET="$(cd "${TARGET:-$DEFAULT_TARGET}" && pwd)"
A="$OS/adapters"

run() { if [[ $DRY -eq 1 ]]; then echo "  [dry-run] $*"; else "$@"; fi; }

# put SRC DEST — copy one file, backing up a different existing DEST.
put() {
  local src="$1" dest="$2"
  run mkdir -p "$(dirname "$dest")"
  if [[ -f "$dest" ]] && ! cmp -s "$src" "$dest"; then
    run cp "$dest" "$dest.bak"
    echo "  backup  ${dest#"$TARGET"/}.bak"
  fi
  run cp "$src" "$dest"
  echo "  wrote   ${dest#"$TARGET"/}"
}

# put_dir SRC_DIR DEST_DIR — copy every file under SRC_DIR.
put_dir() {
  local src="$1" dest="$2" f
  while IFS= read -r -d '' f; do
    put "$f" "$dest/${f#"$src"/}"
  done < <(find "$src" -type f -print0)
}

guard() {
  put "$A/hooks/guard_shell.py" "$1/guard_shell.py"
  run chmod +x "$1/guard_shell.py"
}

sync_cursor() {
  echo "Cursor → $TARGET"
  [[ "${IN_ALL:-0}" == 1 ]] || put "$A/cursor/AGENTS.md" "$TARGET/AGENTS.md"
  put_dir "$A/cursor/rules" "$TARGET/.cursor/rules"
  [[ "${IN_ALL:-0}" == 1 ]] || put_dir "$A/skills" "$TARGET/.cursor/skills"
  put "$A/cursor/hooks.json" "$TARGET/.cursor/hooks.json"
  put_dir "$A/cursor/hooks" "$TARGET/.cursor/hooks"
  run chmod +x "$TARGET"/.cursor/hooks/*.sh 2>/dev/null || true
  guard "$TARGET/.cursor/hooks"
}

sync_claude() {
  echo "Claude Code → $TARGET"
  put "$A/claude/CLAUDE.md" "$TARGET/CLAUDE.md"
  put "$A/claude/settings.json" "$TARGET/.claude/settings.json"
  put_dir "$A/skills" "$TARGET/.claude/skills"
  put_dir "$A/claude/agents" "$TARGET/.claude/agents"
  guard "$TARGET/.claude/hooks"
}

sync_codex() {
  echo "Codex → $TARGET"
  put "$A/codex/AGENTS.md" "$TARGET/AGENTS.md"
  put "$A/codex/config.toml" "$TARGET/.codex/config.toml"
  put "$A/codex/hooks.json" "$TARGET/.codex/hooks.json"
  put_dir "$A/skills" "$TARGET/.agents/skills"
  guard "$TARGET/.codex/hooks"
}

sync_copilot() {
  echo "GitHub Copilot → $TARGET"
  put "$A/copilot/copilot-instructions.md" "$TARGET/.github/copilot-instructions.md"
  put_dir "$A/copilot/instructions" "$TARGET/.github/instructions"
  put_dir "$A/copilot/agents" "$TARGET/.github/agents"
  put_dir "$A/skills" "$TARGET/.github/skills"
}

case "$ADAPTER" in
  cursor) sync_cursor ;;
  claude) sync_claude ;;
  codex) sync_codex ;;
  copilot) sync_copilot ;;
  all)
    # Cursor and Copilot already read .claude/skills and .agents/skills, so the shared
    # skills go only where Claude Code and Codex look for them.
    IN_ALL=1 sync_cursor
    sync_claude
    sync_codex   # writes the lean AGENTS.md last: it is the one shared by every tool
    put "$A/copilot/copilot-instructions.md" "$TARGET/.github/copilot-instructions.md"
    put_dir "$A/copilot/instructions" "$TARGET/.github/instructions"
    put_dir "$A/copilot/agents" "$TARGET/.github/agents"
    ;;
  *) echo "Usage: $0 {cursor|claude|codex|copilot|all} [target_root] [--dry-run]"; exit 1 ;;
esac

echo "Done. Next: python3 ${OS#"$TARGET"/}/tools/bootstrap.py"
