<!-- Purpose: List project scripts and explain their outputs and evidence paths. -->
# Lab scripts

- `scripts/build.ps1` / `.sh`: compile COBOL, Rust, and JDK REST facade.
- `scripts/build-quarkus.ps1`: compile and package Quarkus.
- `scripts/run.ps1` / `.sh`: run standalone JDK service.
- `scripts/run-quarkus.ps1` / `.sh`: run Quarkus.
- `scripts/verify.ps1` / `.sh`: build, test, run Qiskit, and probe PQC.
- `scripts/benchmark.ps1`: benchmark the integrated service.
- `granite/run_eval.ps1`: evaluate the fixed local Granite dataset.
- `pqc/probe.ps1`: inspect PQC algorithms in the selected OpenSSL.
- `scripts/redhat/deploy-openshift.ps1`: build/deploy to OpenShift and save evidence.

Scripts store structured results under `data/results/`; tests use synthetic data.
