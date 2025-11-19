Param(
  [string]$ComposeFile = "docker\compose.yml"
)
Write-Host "Stopping and removing DB + volume..." -ForegroundColor Yellow
docker compose -f $ComposeFile down -v
$env:POSTGRES_PASSWORD = $env:POSTGRES_PASSWORD -as [string]
if (-not $env:POSTGRES_PASSWORD) { $env:POSTGRES_PASSWORD = "changeme" }
docker compose -f $ComposeFile up -d
Write-Host "DB reset complete. Init scripts will run on first boot." -ForegroundColor Green

#powershell -ExecutionPolicy Bypass -File scripts\db_reset.ps1
