#!/usr/bin/env bash
# Sync adapter files into the host project from canonical rigor-os/adapters.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OS="$ROOT/rigor-os"
TARGET="${2:-$ROOT}"
ADAPTER="${1:-cursor}"

sync_cursor() {
  mkdir -p "$TARGET/.cursor/rules" "$TARGET/.cursor/skills" "$TARGET/.cursor/hooks"
  cp "$OS/adapters/cursor/AGENTS.md" "$TARGET/AGENTS.md"
  cp "$OS/adapters/cursor/rules/"*.mdc "$TARGET/.cursor/rules/"
  cp -R "$OS/adapters/cursor/skills/." "$TARGET/.cursor/skills/"
  cp "$OS/adapters/cursor/hooks.json" "$TARGET/.cursor/hooks.json"
  if [[ -d "$OS/adapters/cursor/hooks" ]]; then
    cp -R "$OS/adapters/cursor/hooks/." "$TARGET/.cursor/hooks/"
  fi
  echo "Cursor adapter synced to $TARGET"
}

sync_claude() {
  mkdir -p "$TARGET/.claude/skills" "$TARGET/.claude/agents"
  cp "$OS/adapters/claude/CLAUDE.md" "$TARGET/CLAUDE.md"
  cp "$OS/adapters/claude/settings.json" "$TARGET/.claude/settings.json"
  cp -R "$OS/adapters/claude/skills/." "$TARGET/.claude/skills/" 2>/dev/null || true
  cp -R "$OS/adapters/claude/agents/." "$TARGET/.claude/agents/" 2>/dev/null || true
  echo "Claude adapter synced to $TARGET"
}

sync_codex() {
  mkdir -p "$TARGET/.codex"
  cp "$OS/adapters/codex/AGENTS.md" "$TARGET/AGENTS.md"
  cp "$OS/adapters/codex/config.toml" "$TARGET/.codex/config.toml"
  cp "$OS/adapters/codex/hooks.json" "$TARGET/.codex/hooks.json"
  echo "Codex adapter synced to $TARGET"
}

sync_copilot() {
  mkdir -p "$TARGET/.github/instructions"
  cp "$OS/adapters/copilot/copilot-instructions.md" "$TARGET/.github/copilot-instructions.md"
  cp "$OS/adapters/copilot/instructions/"*.md "$TARGET/.github/instructions/" 2>/dev/null || true
  echo "Copilot adapter synced to $TARGET"
}

case "$ADAPTER" in
  cursor) sync_cursor ;;
  claude) sync_claude ;;
  codex) sync_codex ;;
  copilot) sync_copilot ;;
  all) sync_cursor; sync_claude; sync_codex; sync_copilot ;;
  *) echo "Usage: $0 {cursor|claude|codex|copilot|all} [target_root]"; exit 1 ;;
esac
