#!/usr/bin/env bash

set -euo pipefail

if [ $# -eq 0 ]; then
    echo "Usage: $0 <prompt>" >&2
    exit 1
fi

PROMPT="$*"

claude --print "$PROMPT"
