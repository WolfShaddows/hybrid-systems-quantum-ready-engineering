#!/usr/bin/env bash
# Purpose: run quarkus (scripts/run-quarkus.sh). Expected: check prerequisites, run the corresponding project command, and return its status.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT/scripts/build.sh"
export COBOL_ENGINE="$ROOT/build/txn-engine"
export RUST_ADAPTER="$ROOT/rust/target/release/txn-adapter"
export RUST_LIBRARY="$ROOT/rust/target/release/libhybrid_rust_adapter.so"
export LEDGER_PATH="${LEDGER_PATH:-$ROOT/data/transactions.chain}"
cd "$ROOT"
exec "$ROOT/mvnw" -f java/pom.xml quarkus:dev




