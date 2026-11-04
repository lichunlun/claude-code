#!/usr/bin/env bash
# Research Command Center - one-click start (macOS / Linux)
set -e
cd "$(dirname "$0")"
export PYTHONUTF8=1
if [ ! -x ".venv/bin/python" ]; then
  echo "[RCC] First run: creating Python virtual environment in .venv ..."
  PY=$(command -v python3 || command -v python)
  if [ -z "$PY" ]; then echo "[RCC] ERROR: Python 3.11+ not found."; exit 1; fi
  "$PY" -m venv .venv || { echo "[RCC] ERROR: could not create venv (on Debian/Ubuntu: sudo apt install python3-venv)"; exit 1; }
fi
exec .venv/bin/python scripts/launcher.py start "$@"
