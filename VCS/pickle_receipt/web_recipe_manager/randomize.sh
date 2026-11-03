#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT="${SCRIPT_DIR}"
ENV_FILE="${REPO_ROOT}/.env"
FLAG_FILE="${REPO_ROOT}/flag.txt"

APP_ENCRYPTION_KEY=$(openssl rand -base64 32 | tr '+/' '-_' | tr -d '\n')
FLAG_VALUE="flag{$(cat /proc/sys/kernel/random/uuid)}"

{
    printf "APP_ENCRYPTION_KEY=%s\n" "${APP_ENCRYPTION_KEY}"
} > "${ENV_FILE}"

printf "%s\n" "${FLAG_VALUE}" > "${FLAG_FILE}"

echo "Wrote ${ENV_FILE}"
echo "APP_ENCRYPTION_KEY -> (hidden)"
echo "flag.txt -> ${FLAG_VALUE}"
echo "You can now run \`docker compose build --no-cache\` to rebuild."
