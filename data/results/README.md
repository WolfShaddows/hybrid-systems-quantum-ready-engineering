<!-- Purpose: Inventory machine-readable evidence and provide independent reproduction commands. -->
# Experiments and evidence ledger

JSON artifacts are the source of truth; CSV files are derived exports. Reports record tools, environment, measurements, results, and limitations. Reproduce with `scripts/verify.ps1`, `scripts/verify.ps1 -RunGranite`, or individual commands. `verification-summary.json` stores SHA-256 hashes and passed checks. Hashes identify files but do not prove scientific validity.

| Artifact | Scope | Reproduction |
|---|---|---|
| `verification-summary.json` | Build, six tests, environment, evidence hashes | `python scripts/check_evidence.py` |
| `enterprise-benchmark.json` | 100 local requests; 12.189 req/s; p50 78.588 ms; p95 99.157 ms | `python scripts/benchmark.py` |
| `quarkus-smoke.json` | Quarkus → Java/JNA → Rust ABI → COBOL | `python -m unittest discover -s tests -v` |
| `qiskit-circuits.json` | Eight seeded Bell/GHZ/Grover/noise/scale circuits | `python qiskit/run_experiments.py` |
| `pqc-openssl-capabilities.json` | OpenSSL 3.1.0 listing did not detect tested PQC names | `python pqc/scripts/probe_openssl.py` |
| `granite-evaluation.json` | Two local tags; five synthetic prompts; exact arithmetic 2/3 each | `python granite/run_eval.py` |
| `redhat-openshift-deployment.json` | OpenShift 4.22.22 deployment; completed build, ready pod, bound 1 GiB PVC, HTTPS health, and two synthetic transactions | `oc get builds,imagestreams,pods,svc,routes,pvc`; see `redhat/README.md` |

Granite keyword scores need human review. The OpenSSL listing is not an operation, interoperability, or FIPS test. Qiskit Aer is classical simulation, not QPU. API benchmark omits TLS/network and CPU/RAM. The OpenShift deployment is a single-replica shared Sandbox run; it is not production validation or Red Hat certification.
