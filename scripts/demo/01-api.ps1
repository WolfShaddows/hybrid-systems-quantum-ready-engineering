# Purpose: 01 api (scripts/demo/01-api.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
# Expected: Show the API startup log in the first dedicated demo terminal.
# Stages: Set the window title; move to project root; invoke the existing build-and-run script.
$ErrorActionPreference='Stop'
$root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Host.UI.RawUI.WindowTitle='Hybrid Lab | 1 API service'
Set-Location $root
& (Join-Path $root 'scripts\run-quarkus.ps1')


