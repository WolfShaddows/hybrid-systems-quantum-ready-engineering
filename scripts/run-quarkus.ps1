# Purpose: run quarkus (scripts/run-quarkus.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
& (Join-Path $root 'scripts\build.ps1')
$cobc=Get-Command cobc -ErrorAction Stop
$env:COB_CONFIG_DIR=Join-Path (Split-Path -Parent (Split-Path -Parent $cobc.Source)) "config"
$env:COBOL_ENGINE=Join-Path $root 'build\txn-engine.exe'
$env:RUST_ADAPTER=Join-Path $root 'rust\target\release\txn-adapter.exe'
$env:RUST_LIBRARY=Join-Path $root 'rust\target\release\hybrid_rust_adapter.dll'
$env:LEDGER_PATH=Join-Path $root 'data\transactions.chain'
Push-Location $root
try { & "$root\mvnw.cmd" -f java\pom.xml quarkus:dev }
finally { Pop-Location }





