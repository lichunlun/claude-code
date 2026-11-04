#!/usr/bin/env bash
cd "$(dirname "$0")"
[ -x .venv/bin/python ] || { echo '[RCC] Run ./start.sh once first.'; exit 1; }
exec .venv/bin/python scripts/backup_db.py "$@"
