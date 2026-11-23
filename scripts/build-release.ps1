$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root '.venv\Scripts\python.exe'
if (!(Test-Path -LiteralPath $Python)) {
    throw "Project Python environment not found: $Python"
}
$ReleaseDir = Join-Path $Root 'release'
$BuildDir = Join-Path $Root 'build-release'
$DistDir = Join-Path $Root 'dist-release'
$StageDir = Join-Path $ReleaseDir 'Souline-v1.0.1-win-x64'
$ZipPath = Join-Path $ReleaseDir 'Souline-v1.0.1-win-x64.zip'
Set-Location $Root

& $Python scripts\generate-third-party-inventory.py
if ($LASTEXITCODE -ne 0) { throw "Third-party inventory generation failed" }
& (Join-Path $PSScriptRoot 'verify.ps1')
if (!(Test-Path -LiteralPath $ReleaseDir)) { New-Item -ItemType Directory -Path $ReleaseDir | Out-Null }
if (Test-Path -LiteralPath $StageDir) { Remove-Item -LiteralPath $StageDir -Recurse -Force }
if (Test-Path -LiteralPath $ZipPath) { Remove-Item -LiteralPath $ZipPath -Force }
if (Test-Path -LiteralPath (Join-Path $ReleaseDir 'SHA256SUMS.txt')) {
    Remove-Item -LiteralPath (Join-Path $ReleaseDir 'SHA256SUMS.txt') -Force
}
if (Test-Path -LiteralPath $BuildDir) { Remove-Item -LiteralPath $BuildDir -Recurse -Force }
if (Test-Path -LiteralPath $DistDir) { Remove-Item -LiteralPath $DistDir -Recurse -Force }
& $Python -m PyInstaller --clean --noconfirm --workpath $BuildDir --distpath $DistDir Souline.spec
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed" }

New-Item -ItemType Directory -Path $StageDir | Out-Null
Copy-Item -Path (Join-Path $DistDir 'Souline\*') -Destination $StageDir -Recurse
Copy-Item -LiteralPath (Join-Path $Root 'LICENSE') -Destination $StageDir
Copy-Item -LiteralPath (Join-Path $Root 'THIRD_PARTY_NOTICES.md') -Destination $StageDir
Copy-Item -LiteralPath (Join-Path $Root 'THIRD_PARTY_INVENTORY.md') -Destination $StageDir
Copy-Item -LiteralPath (Join-Path $Root 'TRADEMARKS.md') -Destination $StageDir
Copy-Item -LiteralPath (Join-Path $Root 'RELEASE_NOTES_v1.0.1.md') -Destination $StageDir
Copy-Item -LiteralPath (Join-Path $Root 'third_party_licenses') -Destination $StageDir -Recurse

if (Test-Path -LiteralPath $ZipPath) { Remove-Item -LiteralPath $ZipPath -Force }
Compress-Archive -LiteralPath $StageDir -DestinationPath $ZipPath -CompressionLevel Optimal
$Hash = (Get-FileHash -LiteralPath $ZipPath -Algorithm SHA256).Hash.ToLowerInvariant()
"$Hash  Souline-v1.0.1-win-x64.zip" | Set-Content -LiteralPath (Join-Path $ReleaseDir 'SHA256SUMS.txt') -Encoding ascii
# Per-user installer (Inno Setup 6). Skipped if Inno Setup is not installed.
$Iscc = Join-Path $env:LOCALAPPDATA 'Programs\Inno Setup 6\ISCC.exe'
if (Test-Path -LiteralPath $Iscc) {
    & $Iscc (Join-Path $Root 'installer\Souline.iss')
    if ($LASTEXITCODE -ne 0) { throw "Installer build failed" }
    $SetupPath = Join-Path $ReleaseDir 'Souline-Setup-v1.0.1.exe'
    $SetupHash = (Get-FileHash -LiteralPath $SetupPath -Algorithm SHA256).Hash.ToLowerInvariant()
    "$SetupHash  Souline-Setup-v1.0.1.exe" | Add-Content -LiteralPath (Join-Path $ReleaseDir 'SHA256SUMS.txt') -Encoding ascii
}
Write-Output "Release: $ZipPath"
