# Purpose: build quarkus (scripts/build-quarkus.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
& (Join-Path $root 'scripts\build.ps1')
Push-Location $root
try { & "$root\mvnw.cmd" -f java\pom.xml package; if($LASTEXITCODE -ne 0){throw 'Quarkus packaging failed'} }
finally { Pop-Location }



