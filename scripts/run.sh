#!/usr/bin/env bash
# Purpose: run (scripts/run.sh). Expected: check prerequisites, run the corresponding project command, and return its status.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT/scripts/build.sh"
export COBOL_ENGINE="$ROOT/build/txn-engine"
export RUST_ADAPTER="$ROOT/rust/target/release/txn-adapter"
export LEDGER_PATH="${LEDGER_PATH:-$ROOT/data/transactions.chain}"
cd "$ROOT"
exec java -cp "$ROOT/build/java" org.hybridlab.Main



