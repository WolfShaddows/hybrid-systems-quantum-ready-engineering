# Purpose: 02 traffic (scripts/demo/02-traffic.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
# Expected: Print each HTTP outcome so the journal and health monitors can be observed live.
# Stages: Wait for /health; alternate safe credit/debit requests; attach unique idempotency keys; repeat until Ctrl+C.
$ErrorActionPreference='Stop'
$root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Host.UI.RawUI.WindowTitle='Hybrid Lab | 2 Transaction traffic'
$base='http://127.0.0.1:8080'
while($true){try{$null=Invoke-RestMethod "$base/health" -TimeoutSec 2; break}catch{Write-Host 'Waiting for API startup...'; Start-Sleep 2}}
$step=0
while($true){
  $step++
  $operation=if($step%2 -eq 1){'CREDIT'}else{'DEBIT'}
  $amount=if($operation -eq 'CREDIT'){125}else{40}
  $body=@{account_id='live-demo';idempotency_key=('demo-'+[guid]::NewGuid().ToString('N'));operation=$operation;amount_cents=$amount}|ConvertTo-Json -Compress
  try{$result=Invoke-RestMethod "$base/transactions" -Method Post -ContentType 'application/json' -Body $body -TimeoutSec 10; Write-Host "$(Get-Date -Format T) $($result.status) $operation $amount cents => balance $($result.balance_cents)"}
  catch{Write-Host "$(Get-Date -Format T) REQUEST ERROR: $_" -ForegroundColor Red}
  Start-Sleep -Seconds 2
}


