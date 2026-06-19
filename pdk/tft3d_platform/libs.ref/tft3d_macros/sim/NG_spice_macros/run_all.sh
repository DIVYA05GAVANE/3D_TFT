#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 scripts/run_decks.py
python3 scripts/build_cdslib.py
