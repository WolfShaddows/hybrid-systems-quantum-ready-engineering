# Purpose: run (scripts/run.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $root 'build\txn-engine.exe')) -or -not (Test-Path (Join-Path $root 'build\java\org\hybridlab\Main.class'))) { & (Join-Path $PSScriptRoot 'build.ps1') }
Push-Location $root
try {
  $cobc = Get-Command cobc -ErrorAction Stop
  $env:COB_CONFIG_DIR = Join-Path (Split-Path -Parent (Split-Path -Parent $cobc.Source)) "config"
  $env:COBOL_ENGINE = Join-Path $root 'build\txn-engine.exe'
  $env:RUST_ADAPTER = Join-Path $root 'rust\target\release\txn-adapter.exe'
  $env:LEDGER_PATH = Join-Path $root 'data\transactions.chain'
  java -cp (Join-Path $root 'build\java') org.hybridlab.Main
}
finally { Pop-Location }




