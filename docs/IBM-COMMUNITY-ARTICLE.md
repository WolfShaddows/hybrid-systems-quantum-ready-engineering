# Hybrid Systems and Quantum-Ready Engineering: A Reproducible Lab

**Independent Engineering Research | November 2026**

## 1. Executive Summary

Modernizing enterprise systems does not necessarily require replacing established technologies. In many cases, the more practical challenge is integrating existing transactional capabilities with modern programming languages, APIs, artificial intelligence, cryptographic technologies, and cloud-native infrastructure.

This independent engineering project explores that challenge through a reproducible hybrid laboratory combining COBOL, Rust, Java, IBM Granite, Qiskit Aer, OpenSSL, and Red Hat OpenShift.

The work is organized into five independent technical areas:

- Enterprise modernization through COBOL, Rust, and Java interoperability.
- Local AI-assisted engineering and reproducible IBM Granite evaluation.
- Post-quantum cryptography capability exploration.
- Quantum circuit simulation using Qiskit Aer.
- Cloud-native deployment and transaction verification on Red Hat OpenShift.

The principal contribution is not a claim of production readiness or technological superiority. It is an integrated engineering experiment supported by source code, test cases, machine-readable reports, environment details, execution commands, and documented limitations.

One result deserves particular attention: the hybrid application was successfully built and deployed on a real Red Hat OpenShift Developer Sandbox cluster. Its HTTPS endpoint was verified, persistent storage was bound, and synthetic transactions were successfully processed through the deployed application.

All results presented here are limited to the specific configurations and experiments documented in the repository.

## 2. Results at a Glance

The laboratory produced the following results across its independent workstreams.

| Workstream | Result |
|---|---|
| COBOL + Rust + Java | Integrated transaction-processing path verified |
| Transaction verification | Six integration tests passed |
| Local IBM Granite evaluation | Two local model configurations evaluated |
| Qiskit Aer | Eight experiment cases passed their assertions |
| OpenSSL PQC capability probe | Algorithm availability inspection completed |
| Red Hat OpenShift | Build completed and application deployed successfully |
| OpenShift runtime | Pod running and ready, 1/1 container |
| Persistent storage | 1 GiB PersistentVolumeClaim bound |
| HTTPS endpoint | Health check returned `status=ok` |
| Deployed transactions | 700-cent credit and 250-cent debit successfully posted |
| Final transaction balance | 450 cents |

These results describe separate experiments and must not be interpreted as a single universal performance benchmark.

The OpenShift deployment is particularly relevant because it moves the project beyond local execution: the application was built by OpenShift, deployed to a shared cluster, exposed through an HTTPS Route, and exercised with actual requests against the deployed endpoint.

The deployment was verified through machine-readable evidence rather than relying exclusively on screenshots or visual demonstrations.

## 3. Enterprise Modernization: COBOL, Rust and Java

The central architecture explores how an established transaction-processing language can participate in a modern application environment.

The implemented transaction path is:

```text
HTTP Client
    |
    v
Java / Quarkus API
    |
    +---- JNA / C ABI
    |         |
    |         v
    |       Rust Adapter
    |         |
    |         v
    |       COBOL Rules Engine
    |
    +---- Local SHA-256 Hash-Chained Journal
```

Each component has a defined responsibility.

**COBOL**

Implements the transaction rules, including credits, debits, insufficient-funds handling, and overflow conditions.

**Rust**

Provides the native adapter responsible for validating arguments and invoking the COBOL component.

**Java and Quarkus**

Expose the application API, validate JSON contracts, handle idempotency, and manage the laboratory's local state.

Java also independently recalculates transaction decisions before accepting events.

**Local transaction journal**

Records events through an append-only, SHA-256 hash-chained structure protected by a writer lock.

An important architectural distinction must be emphasized: COBOL is the transaction rules engine in this implementation, while Java persists the laboratory's local state.

This is a prototype integration. It is not connected to IBM Z, z/OS, Enterprise COBOL, or an existing banking ledger.

### Transaction verification

The Quarkus smoke test exercised the native integration path:

```text
CREDIT 980 → POSTED, balance_cents=980
DEBIT  980 → POSTED, balance_cents=0
adapter    → native-ffi
```

The integration suite covered:

- Idempotency.
- Conflicting requests.
- Insufficient funds.
- Invalid input.
- Concurrent requests.
- Journal tampering.

The latest recorded verification passed six tests.

Evidence:

`data/results/quarkus-smoke.json`

`data/results/verification-summary.json`

The objective is to demonstrate a clearly defined division of responsibilities rather than simply combining languages in the same application.

## 4. IBM Granite: Local AI-Assisted Engineering Evaluation

IBM Granite was integrated as a local technical review component through Ollama.

Two local model tags were evaluated:

- `granite42-fast:latest`
- `granite42-think:latest`

The evaluation used synthetic engineering cases covering:

- Exact arithmetic.
- Boundary-condition bug detection.
- SQL injection identification.
- Abstention when a source did not provide sufficient information.
- Repeatability of an arithmetic case.

The retained evaluation artifacts include prompts, raw responses, latency measurements, and model fingerprints.

### Observed results

| Metric | Granite Fast | Granite Think |
|---|---:|---:|
| Exact arithmetic | 2/3 | 2/3 |
| Bug detection, keyword proxy | 1/1 | 1/1 |
| Security finding, keyword proxy | 1/1 | 1/1 |
| Abstention after reviewing raw answer | 1/1 | 1/1 |
| Agreement on repeated arithmetic case | 1/1 | 1/1 |
| Mean observed local latency | 16,258.82 ms | 14,392.05 ms |

The arithmetic evaluation revealed an important limitation.

Both configurations failed the second exact calculation:

```text
Input:
(9800 - 2750) + 125

Correct result:
7175 cents

Granite Fast:
7275 cents

Granite Think:
10675 cents
```

These incorrect responses were retained in the evaluation artifacts rather than excluded from the results.

The experiment also identified a false negative in the initial evaluator. Granite Fast correctly stated that the source did not establish the availability percentage and that it could not be determined, but the original keyword-based rubric failed to recognize those expressions.

We expanded the rubric and rescored the retained responses without executing inference again.

The evaluation report records this correction:

- Original responses preserved.
- Evaluation rubric expanded.
- Results rescored.
- `new_inference_run` set to `false`.

This is an important methodological point: an evaluation system must itself be evaluated. Otherwise, the measurement process can introduce errors that are incorrectly attributed to the model.

The security result is a keyword-based proxy, not an independent security audit.

These results apply only to the tested dataset, local tags, Ollama 0.40.16, and the host environment. They do not establish a general ranking of IBM Granite models or a controlled comparison across all model configurations.

Our architectural principle is straightforward: AI can assist engineering review, but deterministic computation, independent verification, and human oversight remain responsible for accepting results.

Evidence:

`data/results/granite-evaluation.json`

`granite/dataset/cases.json`

## 5. Quantum Computing Experiments with Qiskit Aer

A separate workstream explored quantum circuit behavior through Qiskit and Qiskit Aer.

The recorded environment was:

- Qiskit 2.4.1.
- Qiskit Aer 0.17.2.
- Base random seed: `20261117`.
- 4,096 shots per circuit.

The experiment suite included:

- Two-qubit Bell state.
- Three-qubit GHZ state.
- Grover search for `11`.
- Bell circuit with depolarizing noise.
- GHZ circuits with increasing qubit counts, from two to twelve.

### Selected results

```text
bell_2q_ideal
counts = {00: 2009, 11: 2087}
pass   = true

ghz_3q_ideal
counts = {000: 1993, 111: 2103}
pass   = true

grover_mark_11_2q
counts = {11: 4096}
pass   = true

bell_depolarizing
counts = {00: 2044, 11: 1994, 10: 25, 01: 33}
pass   = true

ghz_12q_scaling
counts = {000000000000: 2046, 111111111111: 2050}
pass   = true
```

All eight experiment cases passed their defined assertions.

The ideal Bell experiment produced correlated outcomes, while the depolarizing-noise experiment introduced additional outcomes under the configured noise model.

The Grover experiment returned the marked state in all recorded simulator shots.

These results demonstrate the expected behavior under the implemented circuit configurations. They do not demonstrate quantum advantage.

**An important limitation:** all experiments ran on the `aer_simulator` backend. This is classical simulation, not execution on a physical quantum processing unit.

The reported execution times are specific to the host environment and include compilation and simulation overhead.

Evidence:

`data/results/qiskit-circuits.json`

`qiskit/run_experiments.py`

## 6. Post-Quantum Cryptography: OpenSSL Capability Exploration

Post-quantum cryptography and quantum computing are related research areas, but they address different problems.

PQC algorithms are designed to run on classical computing systems while providing protection against threats from future quantum-capable adversaries.

They do not require quantum hardware.

This workstream examined the availability of selected NIST-standardized algorithms through a local OpenSSL installation.

The standards considered were:

- ML-KEM — FIPS 203.
- ML-DSA — FIPS 204.
- SLH-DSA — FIPS 205.

The local probe inspected OpenSSL 3.1.0 and did not find the corresponding ML-KEM-512, ML-KEM-768, ML-KEM-1024, ML-DSA, or SLH-DSA names in the reported algorithm listings.

This result must be interpreted narrowly.

It means that the inspected binary did not advertise those algorithm names through the particular listing check performed by the experiment.

It does not establish that:

- The algorithms are unavailable in every OpenSSL build.
- Red Hat Enterprise Linux lacks PQC capabilities.
- A particular Red Hat product is incompatible with these standards.
- A cryptographic operation has failed.
- FIPS validation has been performed.

No cryptographic operation, interoperability test, or FIPS validation was conducted in this phase.

This is a preliminary capability probe that establishes a baseline for future implementation and interoperability testing.

Official standards:

- FIPS 203 — ML-KEM.
- FIPS 204 — ML-DSA.
- FIPS 205 — SLH-DSA.

Evidence:

`data/results/pqc-openssl-capabilities.json`

## 7. Red Hat OpenShift: Successful Cloud-Native Deployment

The Red Hat workstream produced one of the most significant operational results of this laboratory.

Rather than stopping at a local container build or a prepared deployment manifest, the application was built and deployed on a real Red Hat OpenShift Developer Sandbox cluster.

The recorded cluster version was:

`4.22.22`

The deployment used the project:

`wolfshadows-dev-dev`

### Build and deployment

The application was built from the repository's Containerfile.

During the process, we encountered a Rust toolchain compatibility issue: the original Ubuntu package supplied Cargo 1.75, which could not parse the crate's Rust 2024 edition.

The Containerfile was subsequently updated to use a dedicated `rust:1.85-slim` build stage before assembling the COBOL executable, Rust adapter, and Quarkus application into the runtime image.

The deployment script applied the following resources:

- Deployment.
- Service.
- Route.
- PersistentVolumeClaim.

OpenShift completed the build, deployed the application, and reported a ready runtime pod.

### Verified deployment results

| Verification | Observed result |
|---|---|
| OpenShift build | `hybrid-engineering-lab-2` — Complete |
| Runtime pod | Running and ready |
| Container readiness | 1/1 |
| Image digest | `sha256:8fe0f2e132cd9168c6fd3e08d6145f294cca5a266a0329228dd1c35075619648` |
| Persistent storage | `hybrid-engineering-ledger` — Bound |
| Storage allocation | 1 GiB |
| Service | `hybrid-engineering-lab` |
| Service port | 8080 |
| HTTPS health check | `status=ok` |
| Ledger | Append-only hash chain |
| Writer protection | Single-writer lock enabled |
| Runtime decision adapter | `process` |

### End-to-end transaction verification

The deployment script submitted two synthetic transactions through the HTTPS Route.

The results were:

```text
Transaction 1:
Operation: CREDIT
Amount: 700 cents
Result: POSTED
Balance: 700 cents

Transaction 2:
Operation: DEBIT
Amount: 250 cents
Result: POSTED
Balance: 450 cents
```

Both requests returned `POSTED`.

Neither response was an idempotency replay.

The tested requests therefore crossed the deployed OpenShift Route, Quarkus API, application adapter, transaction rules, and persistent journal.

This is an important distinction: the deployment evidence demonstrates more than successful application startup. It records successful transaction processing through the deployed application path.

The results were retained in:

`data/results/redhat-openshift-deployment.json`

The deployment also generated a terminal confirmation:

```text
PASS: OpenShift deployment verified in project wolfshadows-dev-dev; route https://hybrid-engineering-lab-wolfshadows-dev-dev.apps.rm2.thpm.p1.openshiftapps.com
Evidence: C:\Users\PC\Desktop\HYBRID-SYSTEMS-QUANTUM-READY-ENGINEERING\data\results\redhat-openshift-deployment.json
```

### What this deployment demonstrates

The experiment demonstrates that the implemented COBOL, Rust, and Java integration can be packaged and deployed through an OpenShift build workflow and exercised through a cloud-hosted HTTPS endpoint.

It also demonstrates the practical value of testing language interoperability and transaction behavior beyond the local development environment.

This is not a claim of production readiness, but it is a concrete deployment result supported by recorded cluster evidence.

### Red Hat deployment limitations

The deployment ran on shared Red Hat Developer Sandbox infrastructure.

It was not a self-managed RHEL deployment.

The experiment did not evaluate OpenShift Pipelines or Ansible Automation Platform, and it does not establish Red Hat product certification.

The application uses one replica because the hash-chained journal is a local file protected by a process lock. It is not a distributed database and does not provide distributed consensus.

The experiment did not validate:

- Multi-replica consistency.
- Node-failure recovery.
- Storage-failure recovery.
- Production-scale throughput.
- High availability.
- Disaster recovery.
- Production security certification.

The Developer Sandbox environment is temporary, and the live deployment may no longer be available after the trial expires.

Nevertheless, the recorded JSON report preserves the deployment evidence and the steps needed for independent inspection.

## 8. Local API Performance Benchmark

A separate benchmark evaluated the example JDK API through 100 requests in one local process.

Recorded results:

```text
requests   = 100
duration   = 8.204373 seconds
throughput = 12.189 requests/second

Latency:
minimum = 73.780 ms
p50     = 78.588 ms
p95     = 99.157 ms
maximum = 119.299 ms
```

These measurements exclude TLS and external networking.

CPU and memory consumption were not sampled.

The benchmark used the Rust process adapter. It must be distinguished from the separate Quarkus smoke test, which verified the native JNA/ABI integration path.

The measurements are host-specific and should not be extrapolated to production workloads.

Evidence:

`data/results/enterprise-benchmark.json`

## 9. Reproducibility and Technical Evidence

Reproducibility is a central design principle of this project.

The repository retains:

- Source code.
- Synthetic evaluation datasets.
- Test cases.
- Execution scripts.
- Environment and version information.
- Machine-readable JSON reports.
- Model fingerprints and retained responses.
- Deployment evidence.
- Known limitations.
- Reproduction instructions.

The main verification command is:

```powershell
$env:COB_CONFIG_DIR='C:\gnucobol\GnuCOBOL-Win32-MinGW-master\GnuCOBOL-Win32-MinGW-master\config'

.\scripts\verify.ps1
python scripts/benchmark.py
```

The independent workstreams can be executed separately:

```powershell
# IBM Granite evaluation
.\scripts\verify.ps1 -RunGranite

# Qiskit experiments
python qiskit/run_experiments.py

# OpenSSL capability probe
python pqc/scripts/probe_openssl.py

# Red Hat OpenShift deployment
oc project wolfshadows-dev-dev
.\scripts\redhat\deploy-openshift.ps1
```

The OpenShift deployment requires an authenticated OpenShift CLI session and an available project.

The detailed reproduction instructions are documented in:

`data/results/README.md`

The machine-readable reports are intended to allow readers to inspect the findings without depending on screenshots or manually transcribed measurements.

## 10. Architecture Boundaries and Research Limitations

The laboratory intentionally separates its technical workstreams.

This is necessary because each area requires a different form of verification.

**Enterprise modernization**

The transaction path demonstrates language interoperability and defined component responsibilities. It does not demonstrate integration with a production mainframe or existing banking infrastructure.

**AI-assisted engineering**

The Granite evaluation demonstrates behavior on a small, synthetic dataset. It is not a comprehensive benchmark, and keyword-based scoring does not replace human evaluation.

**Quantum computing**

Qiskit Aer results are classical simulations. No physical quantum hardware or quantum advantage was demonstrated.

**Post-quantum cryptography**

The OpenSSL experiment is an algorithm-listing capability probe. No cryptographic interoperability, security assessment, or FIPS validation was performed.

**Red Hat OpenShift**

The deployment demonstrates a working application on shared Developer Sandbox infrastructure. It is not a production deployment, self-managed RHEL evaluation, or certification.

**Performance**

The API measurements are local, limited in scope, and not representative of production infrastructure.

These boundaries are not incidental disclaimers. They define precisely what the project has demonstrated and where further research is required.

## 11. Conclusions: Engineering Modernization Through Measurable Integration

This project explores a practical approach to hybrid engineering.

COBOL, Rust, and Java can participate in a single transaction-processing architecture when their responsibilities and interfaces are explicitly defined.

Local AI models can assist technical review, but their output must be evaluated against independent expectations and human judgment.

Qiskit can provide a controlled environment for studying quantum circuits, while post-quantum cryptography requires its own standards-based implementation and verification process.

Red Hat OpenShift provides the deployment environment in which the hybrid application was built, deployed, exposed through HTTPS, and tested with synthetic transactions.

The most important result is not that every technology was combined into one system. It is that each workstream was given a defined scope, tested with appropriate methods, and documented with evidence.

Modernization should not be understood as replacing established technologies simply because newer alternatives exist.

It should be understood as engineering the interfaces, controls, and verification mechanisms that allow different generations of technology to work together reliably.

The next phase of this research will focus on deeper transaction-contract testing, expanded PQC implementation and interoperability, stronger deployment resilience, and larger-scale reproducibility.

## 12. Project Resources and References

**Source code and evidence**

GitHub repository: [Insert the repository URL]

The repository contains the source code, scripts, test cases, machine-readable reports, and reproduction instructions associated with this research.

**Technology references**

- GnuCOBOL: https://gnucobol.sourceforge.io/
- Rust: https://www.rust-lang.org/
- Python: https://www.python.org/
- Quarkus: https://quarkus.io/
- OpenJDK: https://openjdk.org/
- Ollama: https://ollama.com/
- IBM Granite: https://www.ibm.com/granite
- Qiskit: https://www.ibm.com/quantum/qiskit
- OpenSSL: https://www.openssl.org/
- Red Hat Developer Sandbox: https://developers.redhat.com/developer-sandbox
- Red Hat OpenShift: https://www.redhat.com/en/technologies/cloud-computing/openshift

**Post-quantum cryptography standards**

- NIST FIPS 203 — ML-KEM: https://csrc.nist.gov/pubs/fips/203/final
- NIST FIPS 204 — ML-DSA: https://csrc.nist.gov/pubs/fips/204/final
- NIST FIPS 205 — SLH-DSA: https://csrc.nist.gov/pubs/fips/205/final

---

**Research statement**

This is independent engineering research. It does not imply product endorsement, certification, or institutional collaboration.

All findings are limited to the implementations, configurations, datasets, and experiments described in the repository. The project is published to encourage technical review, reproducibility, and further experimentation.
