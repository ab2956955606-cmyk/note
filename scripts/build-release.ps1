param(
    [string]$Version = "1.1.0",
    [switch]$CreateGitHubRelease
)

$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$CleanVersion = $Version.TrimStart("v")
$Tag = "v$CleanVersion"
$ReleaseDir = Join-Path $Root "release"
$InstallerName = "MyNotes-AI-$Tag-windows-x64.msi"
$HashName = "MyNotes-AI-$Tag-windows-x64.sha256"
$InstallerPath = Join-Path $ReleaseDir $InstallerName
$HashPath = Join-Path $ReleaseDir $HashName
$DesktopDir = Join-Path $Root "apps\desktop"
$TauriTargetDir = Join-Path $DesktopDir "src-tauri\target\release\bundle\msi"

New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null

& (Join-Path $PSScriptRoot "build-web.ps1")
& (Join-Path $PSScriptRoot "build-backend.ps1")

Push-Location $DesktopDir
try {
    if (Test-Path "package-lock.json") {
        npm.cmd ci
        if ($LASTEXITCODE -ne 0) {
            throw "npm ci failed for apps/desktop."
        }
    }
    else {
        npm.cmd install
        if ($LASTEXITCODE -ne 0) {
            throw "npm install failed for apps/desktop."
        }
    }

    & (Join-Path $PSScriptRoot "check-packaging-toolchain.ps1")
    npm.cmd run build
    if ($LASTEXITCODE -ne 0) {
        throw "npm run build failed for apps/desktop."
    }
}
finally {
    Pop-Location
}

$Msi = Get-ChildItem -Path $TauriTargetDir -Filter "*.msi" -Recurse -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Msi) {
    throw "Tauri build did not produce an MSI under $TauriTargetDir"
}

Copy-Item -LiteralPath $Msi.FullName -Destination $InstallerPath -Force
$Hash = Get-FileHash -Algorithm SHA256 -LiteralPath $InstallerPath
Set-Content -Path $HashPath -Value "$($Hash.Hash.ToLower())  $InstallerName" -Encoding ASCII

Write-Host "Release installer: $InstallerPath"
Write-Host "SHA256 file: $HashPath"

if ($CreateGitHubRelease) {
    $NotesPath = Join-Path $Root "docs\release-v1.1.0.md"
    & (Join-Path $PSScriptRoot "check-packaging-toolchain.ps1") -RequireGitHubAuth

    git diff --quiet
    if ($LASTEXITCODE -ne 0) {
        throw "Working tree has uncommitted changes. Commit before publishing a GitHub Release."
    }

    gh.cmd release view $Tag *> $null
    if ($LASTEXITCODE -eq 0) {
        gh.cmd release upload $Tag $InstallerPath $HashPath --clobber
    }
    else {
        gh.cmd release create $Tag $InstallerPath $HashPath --title "MyNotes AI $Tag" --notes-file $NotesPath
    }
}
