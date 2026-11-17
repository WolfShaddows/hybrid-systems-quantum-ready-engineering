# Purpose: 04 health monitor (scripts/demo/04-health-monitor.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
# Expected: Show service availability and whether Java is using Rust native FFI.
# Stages: Request /health on a fixed interval; parse the response; print a timestamped status until Ctrl+C.
$Host.UI.RawUI.WindowTitle='Hybrid Lab | 4 Health monitor'
$uri='http://127.0.0.1:8080/health'
while($true){
  try{$h=Invoke-RestMethod $uri -TimeoutSec 2; Write-Host "$(Get-Date -Format T) status=$($h.status) adapter=$($h.decision_adapter) ledger=$($h.ledger)" -ForegroundColor Green}
  catch{Write-Host "$(Get-Date -Format T) API unavailable: $_" -ForegroundColor Yellow}
  Start-Sleep -Seconds 2
}


