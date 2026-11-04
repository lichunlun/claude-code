#!/usr/bin/env bash
# Stop the app first.  ./restore.sh --list | --latest | --file path
cd "$(dirname "$0")"
[ -x .venv/bin/python ] || { echo '[RCC] Run ./start.sh once first.'; exit 1; }
if [ $# -eq 0 ]; then set -- --list; fi
exec .venv/bin/python scripts/restore_db.py "$@"
