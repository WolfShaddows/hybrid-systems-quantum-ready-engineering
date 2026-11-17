# Purpose: Build and deploy the hybrid lab to an authenticated OpenShift project and save independent runtime evidence.
# Stages: Validate oc -> stage Docker context -> build on cluster -> apply resources -> verify route/health/transactions -> write JSON evidence.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$app = 'hybrid-engineering-lab'
$evidencePath = Join-Path $root 'data\results\redhat-openshift-deployment.json'
$report = [ordered]@{ experiment_id='redhat-openshift-deployment'; status='failed'; timestamp_utc=[DateTime]::UtcNow.ToString('o'); project=$null; cluster_version=$null; image_digest=$null; route=$null; health=$null; transactions=@(); checks=@(); error=$null }
$failed = $false
$stage = $null
$manifestTemp = $null
function Invoke-Oc([string[]]$Arguments) {
  $output = & $script:oc @Arguments 2>&1
  if ($LASTEXITCODE -ne 0) { throw "oc $($Arguments -join ' ') failed ($LASTEXITCODE): $($output -join ' ')" }
  return ($output -join [Environment]::NewLine).Trim()
}
try {
  $script:oc = (Get-Command oc -ErrorAction Stop).Source
  $null = Invoke-Oc @('whoami')
  $report.project = Invoke-Oc @('project','-q')
  $versionText = Invoke-Oc @('version','-o','json')
  try { $report.cluster_version = ($versionText | ConvertFrom-Json).openshiftVersion } catch { $report.cluster_version = $versionText }
  $report.checks += 'oc authentication and active project verified'

  $existing = Invoke-Oc @('get','buildconfig',$app,'--ignore-not-found','-o','name')
  if (-not $existing) {
    $null = Invoke-Oc @('new-build',"--name=$app",'--binary','--strategy=docker')
    $report.checks += 'binary Docker BuildConfig created'
  } else { $report.checks += 'existing BuildConfig reused' }

  $stage = Join-Path $env:TEMP ("hybrid-openshift-" + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Path $stage | Out-Null
  & robocopy $root $stage /E /XD .git .vscode build target node_modules .venv /XF transactions.chain transactions.chain.lock | Out-Null
  if ($LASTEXITCODE -ge 8) { throw "Could not stage build context (robocopy exit $LASTEXITCODE)" }
  Copy-Item -LiteralPath (Join-Path $root 'Containerfile') -Destination (Join-Path $stage 'Dockerfile') -Force
  $buildOutput = Invoke-Oc @('start-build',$app,('--from-dir=' + $stage),'--follow')
  $report.build_log_tail = @($buildOutput -split '\r?\n' | Select-Object -Last 25)
  $buildConfig = Invoke-Oc @('get','buildconfig',$app,'-o','json') | ConvertFrom-Json
  $buildName = "$app-$($buildConfig.status.lastVersion)"
  $buildInfo = Invoke-Oc @('get','build',$buildName,'-o','json') | ConvertFrom-Json
  $report.build = @{ name=$buildName; phase=$buildInfo.status.phase; reason=$buildInfo.status.reason }
  if ($buildInfo.status.phase -ne 'Complete') {
    $failedBuildLog = Invoke-Oc @('logs',("build/" + $buildName))
    $report.build_log_tail = @($failedBuildLog -split '\r?\n' | Select-Object -Last 35)
    throw "OpenShift build $buildName ended in phase '$($buildInfo.status.phase)' (reason: $($buildInfo.status.reason)); see build_log_tail in the evidence JSON"
  }
  $report.checks += 'cluster binary build completed'
  $tagJson = Invoke-Oc @('get','imagestreamtag',($app + ':latest'),'-o','json') | ConvertFrom-Json
  $report.image_digest = $tagJson.image.metadata.name

  $image = "image-registry.openshift-image-registry.svc:5000/$($report.project)/" + $app + ':latest'
  $manifest = Join-Path $root 'redhat\openshift\deployment.yaml'
  $manifestText = Get-Content -LiteralPath $manifest -Raw
  $manifestText = $manifestText.Replace('image-registry.openshift-image-registry.svc:5000/hybrid-lab/hybrid-engineering:latest',$image)
  $manifestTemp = Join-Path $env:TEMP ("hybrid-openshift-manifest-" + [guid]::NewGuid().ToString('N') + '.yaml')
  [IO.File]::WriteAllText($manifestTemp,$manifestText,[Text.UTF8Encoding]::new($false))
  $null = Invoke-Oc @('apply','-f',$manifestTemp)
  $report.checks += 'Deployment, Service, Route, and PVC applied'
  $null = Invoke-Oc @('rollout','status',("deployment/" + $app),'--timeout=300s')
  $podJson = Invoke-Oc @('get','pods','-l',"app.kubernetes.io/name=$app",'-o','json') | ConvertFrom-Json
  $report.pod = @($podJson.items | ForEach-Object { @{ name=$_.metadata.name; phase=$_.status.phase; ready=@($_.status.containerStatuses | Where-Object { $_.ready }).Count -gt 0 } })
  $pvcJson = Invoke-Oc @('get','pvc','hybrid-engineering-ledger','-o','json') | ConvertFrom-Json
  $report.pvc = @{ name=$pvcJson.metadata.name; phase=$pvcJson.status.phase; capacity=$pvcJson.status.capacity.storage }
  $serviceJson = Invoke-Oc @('get','service',$app,'-o','json') | ConvertFrom-Json
  $report.service = @{ name=$serviceJson.metadata.name; cluster_ip=$serviceJson.spec.clusterIP; port=$serviceJson.spec.ports[0].port }
  $routeHost = Invoke-Oc @('get','route',$app,'-o','jsonpath={.spec.host}')
  if (-not $routeHost) { throw 'OpenShift Route has no host' }
  $report.route = "https://$routeHost"
  $report.health = Invoke-RestMethod -Uri ($report.route + '/health') -TimeoutSec 20
  if ($report.health.status -ne 'ok') { throw 'The /health endpoint did not return status=ok' }
  $report.checks += 'Route /health returned status=ok'

  foreach ($item in @(@{operation='CREDIT';amount=700;expected=700},@{operation='DEBIT';amount=250;expected=450})) {
    $request = @{ account_id='openshift-demo'; idempotency_key=('openshift-'+[guid]::NewGuid().ToString('N')); operation=$item.operation; amount_cents=$item.amount } | ConvertTo-Json -Compress
    $result = Invoke-RestMethod -Uri ($report.route + '/transactions') -Method Post -ContentType 'application/json' -Body $request -TimeoutSec 30
    if ($result.status -ne 'POSTED' -or [long]$result.balance_cents -ne $item.expected) { throw "Unexpected $($item.operation) response: $($result | ConvertTo-Json -Compress)" }
    $report.transactions += $result
  }
  $report.checks += 'Synthetic credit and debit returned expected balances'
  $report.status = 'passed'
  Write-Host "PASS: OpenShift deployment verified in project $($report.project); route $($report.route)" -ForegroundColor Green
} catch {
  $failed = $true
  $report.error = $_.Exception.Message
  Write-Error $report.error
} finally {
  New-Item -ItemType Directory -Path (Split-Path -Parent $evidencePath) -Force | Out-Null
  $json = $report | ConvertTo-Json -Depth 12
  [IO.File]::WriteAllText($evidencePath,$json,[Text.UTF8Encoding]::new($false))
  if ($stage -and (Test-Path $stage)) { Remove-Item -LiteralPath $stage -Recurse -Force }
  if ($manifestTemp -and (Test-Path $manifestTemp)) { Remove-Item -LiteralPath $manifestTemp -Force }
  Write-Host "Evidence: $evidencePath"
}
if ($failed) { exit 1 }
