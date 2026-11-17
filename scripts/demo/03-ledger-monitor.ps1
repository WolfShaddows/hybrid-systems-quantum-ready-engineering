# Purpose: 03 ledger monitor (scripts/demo/03-ledger-monitor.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
# Expected: Display new hash-chained records immediately without changing the file.
# Stages: Wait for the ledger to be created; show the latest entries; follow appends until Ctrl+C.
$root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Host.UI.RawUI.WindowTitle='Hybrid Lab | 3 Journal monitor'
$ledger=Join-Path $root 'data\transactions.chain'
Write-Host "Watching read-only journal: $ledger"
while(-not(Test-Path -LiteralPath $ledger)){Write-Host 'Waiting for first transaction...'; Start-Sleep 1}
Get-Content -LiteralPath $ledger -Tail 12 -Wait


