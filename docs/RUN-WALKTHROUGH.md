<!-- Purpose: Explain how to run the lab in six VS Code integrated PowerShell terminals. -->
# Run the lab in six VS Code integrated terminals

Open the project in VS Code. Press **Ctrl+Shift+P**, run **Tasks: Run Task**, and start one task at a time:

| Order | Task | What runs |
|---|---|---|
| 1 | `Hybrid Lab 1 — API service` | Builds and starts Quarkus, Java, Rust, and COBOL. |
| 2 | `Hybrid Lab 2 — Transaction traffic` | Sends synthetic credits/debits every two seconds. |
| 3 | `Hybrid Lab 3 — Journal monitor` | Follows journal records read-only. |
| 4 | `Hybrid Lab 4 — Health monitor` | Polls `/health` and reports the active adapter. |
| 5 | `Hybrid Lab 5 — Granite, Qiskit, PQC` | Runs local Granite, Qiskit, and OpenSSL probes. |
| 6 | `Hybrid Lab 6 — Platform readiness` | Reports local tools and manifest resources; does not deploy. |

Choose **Hybrid Lab — Open all six integrated terminals** to open them together. Tasks 2–4 wait for the API. Stop continuous tasks with **Ctrl+C**.

Alternatively, open one terminal per command from the project root:

```powershell
.\scripts\demo\01-api.ps1
.\scripts\demo\02-traffic.ps1
.\scripts\demo\03-ledger-monitor.ps1
.\scripts\demo\04-health-monitor.ps1
.\scripts\demo\05-research-batch.ps1
.\scripts\demo\06-platform-readiness.ps1
```

Terminal 2 sends requests to Quarkus. Java validates the contract/idempotency, JNA calls Rust through C ABI, Rust invokes COBOL, and Java independently checks the result before appending to the hash-chained journal. Terminals 3–4 observe without changing state.

To verify the COBOL diagnostic:

```powershell
$env:COB_CONFIG_DIR='C:\gnucobol\GnuCOBOL-Win32-MinGW-master\GnuCOBOL-Win32-MinGW-master\config'
.\scripts\verify.ps1
```

The `MAIN-PROCEDURE` paragraph is explicitly invoked from `PROCEDURE DIVISION`. If VS Code retains a stale diagnostic, run **Developer: Reload Window**. Add `-RunGranite` to run local inference; Ollama must have the model tags listed in the report.
