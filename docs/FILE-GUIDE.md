<!-- Purpose: Map maintained project files to their roles and processing stages. -->
# File guide

Maintained source, scripts, manifests, deployment settings, and Markdown include English purpose headers. JSON/CSV retain native syntax so evidence remains parser-compatible.

- `cobol/src/txn_engine.cob`: validate inputs, apply rules, emit structured decision.
- `rust/src/lib.rs`: validate inputs, invoke COBOL, validate response, expose C ABI.
- `java/src/main/java/org/hybridlab/Main.java`: REST, idempotency, Rust call, independent check, hash-chained journal.
- `java/src/main/java/org/hybridlab/NativeAdapter.java`: JNA bridge to Rust C ABI.
- `tests/`: integration and Quarkus smoke checks.
- `.vscode/tasks.json` and `scripts/demo/`: six VS Code terminal roles.
- `granite/`, `qiskit/`, `pqc/`: independent AI, circuit simulation, and OpenSSL experiments.
- `scripts/redhat/deploy-openshift.ps1`: cluster build/deploy, checks, evidence capture.
- `redhat/openshift/deployment.yaml`: Deployment, Service, Route, PVC.
- `Containerfile`: OCI image used by the cluster build.
- `data/results/*.json`: source evidence; CSV files are derived exports.

See [run walkthrough](RUN-WALKTHROUGH.md), [evidence ledger](../data/results/README.md), and [IBM Community article](IBM-COMMUNITY-ARTICLE.md).
