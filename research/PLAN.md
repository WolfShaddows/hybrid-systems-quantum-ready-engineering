<!-- Purpose: Define research methods, workstreams, and acceptance criteria. -->
# Research plan

This research began on November 17, 2026. Deliver a technical synthesis with primary sources, risk/decision inventory, reproducible experiments where possible, negative results and limitations, and future work.

## Method

Form falsifiable hypotheses; prioritize standards and primary vendor documentation; distinguish normative evidence, product docs, local experiments, and inference; define synthetic data, exact commands, environment, expected results, and criteria before running; retain sanitized artifacts; log failures; request independent review.

## Workstreams

- **Enterprise:** define COBOL contract, errors, atomicity, retries, and idempotency; measure bounded Rust/Java integration.
- **AI:** pin Granite model/license/runtime/hardware/prompt/task set; compare with a baseline and require human review. Never use confidential data.
- **PQC:** inventory protocols/dependencies; test specified profiles and measure interoperability, size, latency, memory, and migration. Algorithm presence alone does not prove protocol or FIPS support.
- **Quantum:** run seeded Qiskit circuits; save backend, shots, versions, and statistics; distinguish simulation from PQC.
- **Red Hat:** freeze RHEL/OpenSSL/OpenShift versions/policies. Build/deploy the API on OpenShift; verify image, pod, service, route, health, and synthetic transaction. Store cluster/image/timestamp evidence. Test PQC separately; do not infer OpenShift behavior from RHEL.

Use [the experiment template](../results/EXPERIMENT-TEMPLATE.md). Track progress by acceptance criteria and evidence, not dates.
