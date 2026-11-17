# Purpose: bootstrap maven (scripts/bootstrap-maven.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$version='3.9.16'
$archive="$root\tools\apache-maven-$version-bin.zip"
$base="https://archive.apache.org/dist/maven/maven-3/$version/binaries/apache-maven-$version-bin.zip"
New-Item -ItemType Directory -Force -Path (Join-Path $root 'tools') | Out-Null
Invoke-WebRequest -Uri $base -OutFile $archive
$sumPath="$archive.sha512"; Invoke-WebRequest -Uri "$base.sha512" -OutFile $sumPath
$expected=(Get-Content -LiteralPath $sumPath -Raw).Trim().Split()[0].ToLowerInvariant()
$actual=(Get-FileHash -LiteralPath $archive -Algorithm SHA512).Hash.ToLowerInvariant()
if($expected -ne $actual){throw 'Apache Maven SHA-512 verification failed.'}
Expand-Archive -LiteralPath $archive -DestinationPath (Join-Path $root 'tools') -Force
& "$root\tools\apache-maven-$version\bin\mvn.cmd" --version



