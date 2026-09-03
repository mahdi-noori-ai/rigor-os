#!/usr/bin/env bash
# Cursor beforeShellExecution: deny obvious destructive commands.
set -euo pipefail
payload="$(cat)"
# Default allow if jq missing
if ! command -v jq >/dev/null 2>&1; then
  echo '{"permission":"allow"}'
  exit 0
fi
cmd="$(echo "$payload" | jq -r '.command // empty')"
if echo "$cmd" | grep -Eiq 'rm[[:space:]]+-rf[[:space:]]+/($|[[:space:]])|git[[:space:]]+push.*--force|DROP[[:space:]]+DATABASE|mkfs\.|dd[[:space:]]+if='; then
  jq -n --arg m "Blocked destructive command. Ask the user for explicit approval." \
    '{permission:"deny",user_message:$m,agent_message:$m}'
  exit 0
fi
echo '{"permission":"allow"}'
