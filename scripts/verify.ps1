# Purpose: verify (scripts/verify.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
param([switch]$RunGranite)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
& (Join-Path $PSScriptRoot 'build-quarkus.ps1')
Push-Location $root
try {
  python -m unittest discover -s tests -v
  if($LASTEXITCODE -ne 0){throw 'Integration tests failed'}
  python qiskit\run_experiments.py
  if($LASTEXITCODE -ne 0){throw 'Qiskit experiment failed'}
  python pqc\scripts\probe_openssl.py
  if($LASTEXITCODE -ne 0){throw 'PQC capability probe failed'}
  if($RunGranite){ python granite\run_eval.py; if($LASTEXITCODE -ne 0){throw 'Granite evaluation failed'}; python granite\score_results.py; if($LASTEXITCODE -ne 0){throw 'Granite rescoring failed'} }
  python scripts\export_results_csv.py
  if($LASTEXITCODE -ne 0){throw 'CSV export failed'}
  python scripts\create_verification_summary.py
  if($LASTEXITCODE -ne 0){throw 'Verification summary failed'}
  python scripts\check_evidence.py
  if($LASTEXITCODE -ne 0){throw 'Evidence integrity check failed'}
}
finally { Pop-Location }







