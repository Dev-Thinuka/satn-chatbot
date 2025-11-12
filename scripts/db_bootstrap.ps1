Param(
  [string]$RepoRoot = "C:\Repositories\sa-thomson-chatbot",
  [string]$Container = "satn_pg",
  [string]$Db = "satn_db",
  [string]$User = "satn_admin"
)

$ErrorActionPreference = "Stop"
Write-Host "== SATN DB Bootstrap ==" -ForegroundColor Cyan

# paths
$schemaPath = Join-Path $RepoRoot "docker\init\01-schema.sql"
$seedBase   = Join-Path $RepoRoot "docker\init\02-seed.sql"
$idxPath    = Join-Path $RepoRoot "docker\init\03-indexes.sql"
$seedRich   = Join-Path $RepoRoot "docker\seed\seed_full.sql"

# validate
@($schemaPath, $seedBase, $idxPath, $seedRich) | ForEach-Object {
  if (!(Test-Path $_)) { throw "Missing required SQL file: $_" }
}

if (-not $env:POSTGRES_PASSWORD) {
  throw "POSTGRES_PASSWORD not set. Example: `$env:POSTGRES_PASSWORD='changeme'"
}

# ensure container is running
$running = (docker ps --filter "name=$Container" --format "{{.Names}}") -contains $Container
if (-not $running) {
  Write-Host "Starting compose..." -ForegroundColor Yellow
  Set-Location $RepoRoot
  docker compose -f docker\compose.yml up -d
  Start-Sleep -Seconds 4
}

# helper to run sql file inside container
function Invoke-ContainerSql {
  param(
    [string]$HostFile,
    [string]$ContainerFile = "/tmp/tmp.sql"
  )
  Write-Host " - Copy $(Split-Path -Leaf $HostFile)" -ForegroundColor Yellow
  docker cp $HostFile "$($Container):$ContainerFile" | Out-Null
  Write-Host " - Apply $(Split-Path -Leaf $HostFile)" -ForegroundColor Yellow
  docker exec -e PGPASSWORD=$env:POSTGRES_PASSWORD $Container psql -U $User -d $Db -v ON_ERROR_STOP=1 -f $ContainerFile
}

Write-Host "Applying schema..." -ForegroundColor Cyan
Invoke-ContainerSql -HostFile $schemaPath -ContainerFile "/tmp/01-schema.sql"

Write-Host "Applying base seed..." -ForegroundColor Cyan
Invoke-ContainerSql -HostFile $seedBase -ContainerFile "/tmp/02-seed.sql"

Write-Host "Applying indexes..." -ForegroundColor Cyan
Invoke-ContainerSql -HostFile $idxPath -ContainerFile "/tmp/03-indexes.sql"

Write-Host "Applying rich seed..." -ForegroundColor Cyan
Invoke-ContainerSql -HostFile $seedRich -ContainerFile "/tmp/seed_full.sql"

Write-Host "Verifying counts..." -ForegroundColor Cyan
docker exec -e PGPASSWORD=$env:POSTGRES_PASSWORD $Container `
  psql -U $User -d $Db -c "SELECT 'agents' AS t, COUNT(*) FROM agents
                           UNION ALL SELECT 'properties', COUNT(*) FROM properties
                           UNION ALL SELECT 'users', COUNT(*) FROM users
                           UNION ALL SELECT 'interactions', COUNT(*) FROM interactions
                           ORDER BY 1;"

Write-Host "Bootstrap complete." -ForegroundColor Green
