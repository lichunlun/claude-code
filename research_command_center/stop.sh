#!/usr/bin/env bash
cd "$(dirname "$0")"
[ -x .venv/bin/python ] || { echo '[RCC] Not installed yet.'; exit 0; }
exec .venv/bin/python scripts/launcher.py stop
