# Purpose: probe (pqc/probe.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
param([string]$OpenSsl = 'openssl')
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$env:OPENSSL_BIN=$OpenSsl
Push-Location $root
try { python pqc\scripts\probe_openssl.py }
finally { Pop-Location }



