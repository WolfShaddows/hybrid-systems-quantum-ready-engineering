<!-- Purpose: Define the COBOL, Rust, and Java/API modernization hypothesis and acceptance criteria. -->
# Enterprise modernization: COBOL + Rust + Java/APIs

Layered modernization can preserve COBOL as transaction authority when integration boundaries, schemas, error semantics, idempotency, and reconciliation are explicit and tested.

- **COBOL:** existing rules and transaction behavior as source of truth.
- **Rust:** bounded native component only when measurements justify integration cost.
- **Java/API:** service contract and consumer compatibility; do not silently duplicate rules.

Map transaction/commit boundaries, choose synthetic data, define a versioned API contract, compare service integration with native linking, and record compiler, ABI, encoding, memory ownership, and error behavior. Measure p50/p95/p99, throughput, CPU/memory, failures, retries, and recovery. IBM COBOL/Java and z/OS Connect references do not validate this project's COBOL/Rust bridge.

Expected artifacts: API contract, sanitized examples, architecture/failure diagrams, measurements, and dated platform/compiler matrix. Reject duplicated authority, nondeterminism, unreconciled data, SLO violations, missing observability, duplicate side effects on retry, or unreviewed security.
