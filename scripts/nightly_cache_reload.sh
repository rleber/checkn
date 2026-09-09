#!/bin/bash
#
# Runs checkn's persistent cache reload. Invoked as a job by scheduled_jobs
# (~/projects/sh/scheduled_run/scheduled_jobs), which provides the timeout,
# caffeinate, and logging -- see that script for those. Pulls GITHUB_TOKEN
# (needed by the git domain's cacheable test) from ~/.env.
set -euo pipefail

# Read by ~/.zshrc to skip the oh-my-zsh 1password plugin's op-completion
# regeneration, which can hang non-interactive runs waiting on a TCC prompt.
export CHECKN_NONINTERACTIVE=1

if [ -f "$HOME/.env" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$HOME/.env"
    set +a
fi

exec /Users/richard/.venv/bin/checkn-cache build
