# Purpose: 06 platform readiness (scripts/demo/06-platform-readiness.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
# Expected: Make local Red Hat/container prerequisites visible and report whether a cluster CLI is present.
# Stages: Check oc, Podman, Docker, and OpenSSL; count template resources; explain unavailable runtime capabilities.
$root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Host.UI.RawUI.WindowTitle='Hybrid Lab | 6 Platform readiness'
foreach($tool in @('oc','podman','docker','openssl')){
  $found=Get-Command $tool -ErrorAction SilentlyContinue
  if($found){Write-Host "$tool found: $($found.Source)"}else{Write-Host "$tool unavailable on this host" -ForegroundColor Yellow}
}
$template=Join-Path $root 'redhat\openshift\deployment.yaml'
$count=(Select-String -LiteralPath $template -Pattern '^kind:' | Measure-Object).Count
Write-Host "OpenShift manifest resources: $count (Deployment, Service, Route, PVC)"
Write-Host 'This terminal only checks prerequisites; it does not deploy to a cluster.'


