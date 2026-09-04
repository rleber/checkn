#!/bin/bash
#
# Nightly full reload of checkn's persistent cache. Run via the
# local.checkn.cache-reload LaunchAgent; see
# ~/Library/LaunchAgents/local.checkn.cache-reload.plist. Pulls GITHUB_TOKEN
# (needed by the git domain's cacheable test) from ~/.env.
#
# launchd truncates StandardOutPath/StandardErrorPath on each run rather
# than appending, so this script does its own append-logging instead.
set -euo pipefail

LOG_FILE="$HOME/.checkn_cache_reload.log"

if [ -f "$HOME/.env" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$HOME/.env"
    set +a
fi

{
    echo "=== $(date) ==="
    /Users/richard/.venv/bin/checkn-cache build
    echo "--- done ---"
} >> "$LOG_FILE" 2>&1
