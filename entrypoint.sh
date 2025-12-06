#!/bin/sh

EXECUTED_FROM=$(pwd)
cd $(dirname $0)

set -a
. ./.env
if [ -f .env.local ]; then
    . ./.env.local
fi
set +a

cd "${EXECUTED_FROM}"

exec "$@"

