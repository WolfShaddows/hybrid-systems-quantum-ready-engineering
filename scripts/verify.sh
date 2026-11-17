#!/usr/bin/env bash
# Purpose: verify (scripts/verify.sh). Expected: check prerequisites, run the corresponding project command, and return its status.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT/scripts/build.sh"
python3 -m unittest discover -s "$ROOT/tests" -v
python3 "$ROOT/qiskit/run_experiments.py"
python3 "$ROOT/pqc/scripts/probe_openssl.py"
python3 "$ROOT/scripts/export_results_csv.py"



