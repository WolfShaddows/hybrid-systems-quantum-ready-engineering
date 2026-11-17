# Purpose: build (scripts/build.ps1). Expected: resolve paths, configure local tools, invoke its build/service/experiment/monitor, and report status.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$build = Join-Path $root 'build'
New-Item -ItemType Directory -Force -Path $build,(Join-Path $root 'data') | Out-Null
$cobc = Get-Command cobc -ErrorAction Stop
$config = Join-Path (Split-Path -Parent (Split-Path -Parent $cobc.Source)) 'config'
if (Test-Path -LiteralPath (Join-Path $config 'default.conf')) { $env:COB_CONFIG_DIR = $config }
& $cobc.Source -x -free -o (Join-Path $build 'txn-engine.exe') (Join-Path $root 'cobol\src\txn_engine.cob')
if ($LASTEXITCODE -ne 0) { throw 'GnuCOBOL compilation failed.' }
Push-Location (Join-Path $root 'rust')
try { cargo build --release; if ($LASTEXITCODE -ne 0) { throw 'Rust build failed.' } }
finally { Pop-Location }
$javaOut = Join-Path $build 'java'
New-Item -ItemType Directory -Force -Path $javaOut | Out-Null
$javaSource = Join-Path $root 'java\src\main\java\org\hybridlab\Main.java'
& javac -encoding UTF-8 -d $javaOut $javaSource
if ($LASTEXITCODE -ne 0) { throw 'Java compilation failed.' }
'Build complete: COBOL, Rust, Java.'





