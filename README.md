<!-- Purpose: Introduce the project, its components, evidence, and reproduction commands. -->
# HYBRID SYSTEMS & QUANTUM-READY ENGINEERING

An independent, reproducible lab for enterprise modernization, AI-assisted engineering, post-quantum cryptography (PQC), quantum circuit simulation, and Red Hat technologies.

**Status:** runnable local prototype with evidence generated November 17, 2026. Results describe the environment in each JSON report, not universal product behavior.

## Run in VS Code

Use **Ctrl+Shift+P → Tasks: Run Task** and start Hybrid Lab 1–6 one at a time, or choose **Hybrid Lab — Open all six integrated terminals**. See [.vscode/tasks.json](.vscode/tasks.json), the [walkthrough](docs/RUN-WALKTHROUGH.md), and the [IBM Community article](docs/IBM-COMMUNITY-ARTICLE.md).

## Implemented areas

- **Modernization:** COBOL transaction rules, Rust adapter, Java/Quarkus API, idempotency, and SHA-256 hash-chained journal.
- **AI:** local IBM Granite evaluation on synthetic cases, retained answers, rubric, latency, and limitations.
- **PQC:** local OpenSSL algorithm inventory; missing tested algorithms are reported.
- **Quantum computing:** Qiskit Aer Bell/GHZ/Grover/noise experiments on a classical simulator; no QPU or quantum advantage claim.
- **Red Hat:** OpenShift manifest and server-side build/deployment procedure. Actual cluster deployment is pending successful execution and evidence.

## Local requirements (Windows)

Requires JDK 21+, Python 3.11+, Rust/Cargo, and GnuCOBOL. Install pinned Qiskit/Granite dependencies; Granite also requires Ollama and the model tags in its report.

```powershell
$env:COB_CONFIG_DIR='C:\gnucobol\GnuCOBOL-Win32-MinGW-master\GnuCOBOL-Win32-MinGW-master\config'
.\scripts\verify.ps1
```

Add `-RunGranite` for inference. Run `python scripts/benchmark.py` for the API benchmark.

## Evidence and limits

JSON under [data/results](data/results/README.md) is authoritative; CSV is derived. The local benchmark recorded 12.189 requests/second, p50 78.588 ms, p95 99.157 ms for 100 requests, without TLS/external network. Both Granite tags scored 2/3 on exact arithmetic; incorrect outputs remain documented.

The local GnuCOBOL 2.0 runtime failed `OPEN EXTEND` with status 30 in an environment probe; Java persists the lab journal. OpenSSL 3.1.0 did not advertise tested PQC algorithms. Neither finding characterizes RHEL. The OpenShift manifest is not a deployment until the cluster workflow passes and saves evidence. Experiments are not certification, production readiness, universal benchmark, or evidence of quantum advantage.

## Navigate

[Architecture](docs/ARCHITECTURE.md) · [Decisions](docs/DECISIONS.md) · [Strategy](docs/TECHNICAL-STRATEGY.md) · [Research plan](research/PLAN.md) · [Evidence](data/results/README.md) · [Primary sources](references/SOURCES.md)
