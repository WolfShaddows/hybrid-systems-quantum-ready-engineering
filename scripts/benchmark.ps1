# Purpose: benchmark (scripts/benchmark.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
param([int]$Port = 18080, [int]$Requests = 100)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$env:PORT="$Port"; $env:BENCH_REQUESTS="$Requests"
Push-Location $root
try { python scripts\benchmark.py }
finally { Pop-Location }



