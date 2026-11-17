# Purpose: run eval (granite/run_eval.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
Push-Location $root
try { python granite\run_eval.py @args }
finally { Pop-Location }



