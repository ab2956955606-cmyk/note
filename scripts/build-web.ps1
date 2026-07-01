$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$WebDir = Join-Path $Root "apps\web"

if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) {
    throw "npm.cmd was not found. Install Node.js 20+ before building the web app."
}

Push-Location $WebDir
try {
    if (Test-Path "package-lock.json") {
        npm.cmd ci
        if ($LASTEXITCODE -ne 0) {
            throw "npm ci failed for apps/web."
        }
    }
    else {
        npm.cmd install
        if ($LASTEXITCODE -ne 0) {
            throw "npm install failed for apps/web."
        }
    }

    npm.cmd run build
    if ($LASTEXITCODE -ne 0) {
        throw "npm run build failed for apps/web."
    }
}
finally {
    Pop-Location
}
