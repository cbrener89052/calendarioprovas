#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export DATABASE_URL="${DATABASE_URL:-postgresql://calendario:calendario@localhost:5432/calendario}"
alembic "$@"
