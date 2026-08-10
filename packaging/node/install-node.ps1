param(
  [string]$InstallRoot = "C:\Program Files\AnimusPrimeNode",
  [string]$ServiceName = "AnimusPrimeNode"
)

$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null
Write-Host "Install the pinned Python runtime and requirements-phase1.txt into $InstallRoot\.venv."
Write-Host "Create a machine-scoped environment file with PRIME_NODE_ALLOWED_ROOTS, PRIME_NODE_STATE_FILE, PRIME_NODE_NAME, PRIME_NODE_TLS_CERT_FILE, PRIME_NODE_TLS_KEY_FILE, PRIME_NODE_TLS_CA_FILE, and a one-time PRIME_NODE_BOOTSTRAP_CREDENTIAL."
Write-Host "Register a service wrapper for: python -m apps.node.main"
Write-Host "The packaged service refuses to start without TLS/mTLS files."
Write-Host "Do not put credentials in this script, the repository, or service command-line arguments."
