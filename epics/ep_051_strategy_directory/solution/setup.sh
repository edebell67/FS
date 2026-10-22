#!/usr/bin/env sh
# EP051 deterministic setup. Version 1.0.0 (2026-08-23).
set -eu
cd "$(dirname "$0")"
python3 verify_runtime.py
printf '%s\n' 'EP051 runtime verified. No network install or secret required.'

