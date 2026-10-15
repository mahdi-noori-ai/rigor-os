#!/usr/bin/env bash
# Cursor stop hook: non-blocking; drains the payload and returns no follow-up.
cat >/dev/null
echo '{}'
