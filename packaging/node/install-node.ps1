[CmdletBinding(PositionalBinding = $false)]
param(
  [string]$InstallRoot = "C:\Program Files\AnimusPrimeNode",
  [string]$ServiceName = "AnimusPrimeNode",
  [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")),
  [string]$AllowedRoots,
  [string]$StateFile,
  [string]$NodeName,
  [string]$NodeId,
  [string]$BindHost,
  [int]$Port = 18001,
  [string]$TlsCertFile,
  [string]$TlsKeyFile,
  [string]$TlsCaFile,
  [string]$BootstrapPublicKeyFile,
  [switch]$Start,
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
New-Item -ItemType Directory -Force -Path "$InstallRoot\logs" | Out-Null
$appRoot = "$InstallRoot\app"
New-Item -ItemType Directory -Force -Path $appRoot | Out-Null
Write-Host "Install the pinned Python runtime and requirements-phase1.txt into $InstallRoot\.venv."
$python = "$InstallRoot\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) { throw "Missing pinned runtime: $python" }
$requiredSource = @("apps", "src")
foreach ($item in $requiredSource) {
  $source = Join-Path $SourceRoot $item
  if (-not (Test-Path $source)) { throw "Missing PRIME source directory: $source" }
  Copy-Item -Path $source -Destination $appRoot -Recurse -Force
}
$wrapperSource = Join-Path $PSScriptRoot "windows-service.py"
if (-not (Test-Path $wrapperSource)) { throw "Missing Windows service wrapper: $wrapperSource" }
$wrapper = "$InstallRoot\windows-service.py"
Copy-Item -Path $wrapperSource -Destination $wrapper -Force

$machineSettings = @{
  PRIME_NODE_WINDOWS_SERVICE_NAME = $ServiceName
  PRIME_NODE_ALLOWED_ROOTS = $AllowedRoots
  PRIME_NODE_STATE_FILE = $StateFile
  PRIME_NODE_NAME = $NodeName
  PRIME_NODE_ID = $NodeId
  PRIME_NODE_BIND_HOST = $BindHost
  PRIME_NODE_PORT = if ($Port -gt 0) { [string]$Port } else { $null }
  PRIME_NODE_TLS_CERT_FILE = $TlsCertFile
  PRIME_NODE_TLS_KEY_FILE = $TlsKeyFile
  PRIME_NODE_TLS_CA_FILE = $TlsCaFile
  PRIME_NODE_BOOTSTRAP_PUBLIC_KEY_FILE = $BootstrapPublicKeyFile
}
foreach ($entry in $machineSettings.GetEnumerator()) {
  if (-not [string]::IsNullOrWhiteSpace($entry.Value)) {
    [Environment]::SetEnvironmentVariable($entry.Key, $entry.Value, "Machine")
  }
}

$privateKey = if ($TlsKeyFile) { $TlsKeyFile } else { "$InstallRoot\trust\node.key" }
if (Test-Path $privateKey) {
  & icacls.exe $privateKey /inheritance:r /grant:r "*S-1-5-18:(F)" "*S-1-5-32-544:(F)" | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "failed to protect Node private key ACL" }
}
& icacls.exe "$InstallRoot\data" /inheritance:r /grant:r "*S-1-5-18:(OI)(CI)(F)" "*S-1-5-32-544:(OI)(CI)(F)" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "failed to protect Node state directory ACL" }

$bin = $python.Replace('\','/')
$wrapperBin = $wrapper.Replace('\','/')
$command = "`"$bin`" `"$wrapperBin`""
& sc.exe query $ServiceName | Out-Null
if ($LASTEXITCODE -eq 0) {
  & sc.exe config $ServiceName binPath= $command start= auto DisplayName= "ANIMUS PRIME Node" | Out-Null
} else {
  & sc.exe create $ServiceName binPath= $command start= auto DisplayName= "ANIMUS PRIME Node" | Out-Null
}
if ($LASTEXITCODE -ne 0) { throw "service registration/configuration failed" }
& sc.exe description $ServiceName "Private authenticated ANIMUS PRIME repository Node" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "service description update failed" }
if ($Start) {
  & sc.exe start $ServiceName | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "service start failed" }
}
Write-Host "Registered $ServiceName for automatic startup using the installed PRIME application copy."
Write-Host "Repair is idempotent: rerun with -Repair after updating the package; data and identity are preserved."
Write-Host "The one-time enrollment credential is delivered to /v1/enroll after the mTLS listener starts; it is not stored in service environment or installer logs."
