#!/usr/bin/env bash
# Purpose: build (scripts/build.sh). Expected: check prerequisites, run the corresponding project command, and return its status.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/build" "$ROOT/data"
cobc -x -free -o "$ROOT/build/txn-engine" "$ROOT/cobol/src/txn_engine.cob"
cargo build --release --manifest-path "$ROOT/rust/Cargo.toml"
mkdir -p "$ROOT/build/java"
javac -encoding UTF-8 -d "$ROOT/build/java" "$ROOT/java/src/main/java/org/hybridlab/Main.java"
echo "Build complete: COBOL, Rust, Java"



