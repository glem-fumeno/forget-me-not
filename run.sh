#!/bin/sh

set -a
source ./.env
if [ -f .env.local ]; then
    source ./.env.local
fi
set +a

uv run main.py
