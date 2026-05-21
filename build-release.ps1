param(
  [string]$Version = "0.1.1"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$dist = Join-Path $root "dist"
$staging = Join-Path $dist "MDPASTE-portable-v$Version"
$zipPath = Join-Path $dist "MDPASTE-portable-v$Version.zip"

if (Test-Path -LiteralPath $staging) {
  Remove-Item -LiteralPath $staging -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $staging, $dist | Out-Null

$include = @(
  "MdPaste.exe",
  "_internal",
  "assets",
  "pastemd",
  "MDPASTE.cmd",
  "MdPaste-portable.cmd",
  "portable-config.ps1",
  "switch-startup.cmd",
  "README.md",
  "i18n",
  "RELEASE_NOTES.md",
  "MODIFICATIONS.md",
  "UPSTREAM_COMPARISON.md",
  "SOURCE.md",
  "tools",
  "LICENSE",
  "NOTICE.md"
)

foreach ($item in $include) {
  $source = Join-Path $root $item
  if (-not (Test-Path -LiteralPath $source)) {
    throw "Missing required release item: $item"
  }

  $target = Join-Path $staging $item
  if ((Get-Item -LiteralPath $source).PSIsContainer) {
    Copy-Item -LiteralPath $source -Destination $target -Recurse
  } else {
    Copy-Item -LiteralPath $source -Destination $target
  }
}

New-Item -ItemType Directory -Force -Path (Join-Path $staging "cache") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $staging "portable-data\Roaming") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $staging "portable-data\Local") | Out-Null

if (Test-Path -LiteralPath $zipPath) {
  Remove-Item -LiteralPath $zipPath -Force
}

Compress-Archive -LiteralPath $staging -DestinationPath $zipPath -CompressionLevel Optimal

Write-Host "[OK] Release package created: $zipPath"
