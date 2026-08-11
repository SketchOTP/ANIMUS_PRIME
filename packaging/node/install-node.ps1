param(
  [string]$InstallRoot = "C:\Program Files\AnimusPrimeNode",
  [string]$ServiceName = "AnimusPrimeNode",
  [switch]$Uninstall,
  [switch]$Repair
)

$ErrorActionPreference = "Stop"
if ($Uninstall) {
  & sc.exe stop $ServiceName | Out-Null
  & sc.exe delete $ServiceName | Out-Null
  Write-Host "Removed service $ServiceName. Identity/configuration under the data directory are preserved; remove them separately after an explicit operator decision."
  exit 0
}
New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallRoot\data" | Out-Null
Write-Host "Install the pinned Python runtime and requirements-phase1.txt into $InstallRoot\.venv."
Write-Host "Create a machine-scoped environment file with PRIME_NODE_ALLOWED_ROOTS, PRIME_NODE_STATE_FILE, PRIME_NODE_NAME, PRIME_NODE_TLS_CERT_FILE, PRIME_NODE_TLS_KEY_FILE, PRIME_NODE_TLS_CA_FILE, and a one-time PRIME_NODE_BOOTSTRAP_CREDENTIAL."
$python = "$InstallRoot\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) { throw "Missing pinned runtime: $python" }
$bin = $python.Replace('\','/')
$command = "`"$bin`" -m apps.node.main"
& sc.exe create $ServiceName binPath= $command start= auto DisplayName= "ANIMUS PRIME Node" | Out-Null
& sc.exe description $ServiceName "Private authenticated ANIMUS PRIME repository Node" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "service registration failed" }
Write-Host "Registered $ServiceName for automatic startup. Use sc.exe start/stop/query $ServiceName."
Write-Host "Repair is idempotent: rerun this script after updating the package; it preserves data and identity."
