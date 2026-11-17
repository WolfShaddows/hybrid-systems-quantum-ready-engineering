# Purpose: 05 research batch (scripts/demo/05-research-batch.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
# Expected: Save Granite, Qiskit, and OpenSSL evidence under data/results and print each run's status.
# Stages: Evaluate installed local Granite models; simulate Qiskit circuits; probe OpenSSL PQC listings.
$ErrorActionPreference='Continue'
$root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Host.UI.RawUI.WindowTitle='Hybrid Lab | 5 Research experiments'
Set-Location $root
python granite\run_eval.py
Write-Host "Granite exit code: $LASTEXITCODE"
python qiskit\run_experiments.py
Write-Host "Qiskit exit code: $LASTEXITCODE"
python pqc\scripts\probe_openssl.py
Write-Host "OpenSSL PQC probe exit code: $LASTEXITCODE"


