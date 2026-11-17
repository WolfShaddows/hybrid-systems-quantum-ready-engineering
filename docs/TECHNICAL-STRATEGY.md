<!-- Purpose: Explain implementation strategy, scope risks, and criteria for credible advocacy. -->
# Technical assessment and implementation strategy

The project becomes useful advocacy when broad claims become falsifiable engineering: source code or protocol, retained evidence, predeclared metrics, and an independent reproduction path. Publishing failures and negative results increases credibility.

The scope spans COBOL/Rust/Java, Granite, PQC, Qiskit, OpenSSL, RHEL, OpenShift, and CI/CD. Calling every area complete too soon invites mocks and incomparable measurements. The initial ZIP contained documents and a Qiskit example, not an inherited application.

## Staged approach

1. **Inventory:** identify target machine, available tools, transaction goal, protocol, synthetic data, output schema, versions, and cost limits.
2. **Transaction path:** implement a versioned contract with idempotency, errors, traces, explicit COBOL authority, and an independent oracle. Add load only after correctness and recovery pass.
3. **Independent labs:** freeze Granite tasks and human review; test PQC protocols separately; record Qiskit backend/seed/shots; use OpenShift to build, deploy, route, health-check, and evidence the running API.
4. **Evidence and publication:** version JSON with commit, versions/hashes, configuration, dataset, command, criteria, metrics, status, and limitations. CSV is derived.

An OpenShift manifest is not a deployment. A platform claim needs successful cluster build, pod, route, health check, transaction, and retained evidence. This requires no quantum hardware.

## Article directions

- **Enterprise modernization:** contracts, COBOL authority, integration, correctness, operating cost.
- **Quantum-ready security:** inventory, PQC tests, interoperability, crypto agility, support limits.
- **AI and quantum engineering:** separate studies joined by reproducible evaluation; Qiskit is not the basis for PQC and Granite is not an authority on truth.

## IBM Champions

The lab provides material, but does not itself establish an advocacy record. Pair it with useful IBM Community/TechXchange participation, tutorials, demos, mentoring, and concrete product feedback. Record audience, contribution, and evidence. Check current program criteria; post counts do not guarantee selection.

## Progress criterion

A stage is ready when an independent reader can run the command, get an equivalent result within stated tolerances, verify provenance, and understand limitations. If it cannot be reproduced, record it as blocked or negative with a diagnosis.
