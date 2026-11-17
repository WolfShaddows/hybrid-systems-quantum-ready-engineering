<!-- Purpose: Record binding research and implementation decisions with their rationale. -->
# Research decisions

## D-001 — Separate quantum computing from PQC
Keep documents, tests, metrics, and conclusions separate. PQC runs on classical computers; quantum computing studies circuits that manipulate quantum information.

## D-002 — Keep COBOL authoritative
Integrate through explicit contracts; do not silently duplicate an existing transaction commit. Change authority only with evidence, reconciliation, and rollback plans.

## D-003 — Require human approval for AI changes
AI may propose; tests and human reviewers decide acceptance. Version prompts, models, and configuration.

## D-004 — Use established PQC implementations
Test documented implementations and protocols. Record version, format, and mode; algorithm availability alone does not prove interoperability.

## D-005 — Version product claims
Every statement about RHEL/OpenSSL/OpenShift, Granite/Qiskit, or COBOL compilers needs an applicable source and version.
