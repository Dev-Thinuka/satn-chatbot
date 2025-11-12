Param(
  [string]$RepoRoot = "C:\Repositories\sa-thomson-chatbot",
  [string]$Container = "satn_pg",
  [string]$Db = "satn_db",
  [string]$User = "satn_admin"
)

$ErrorActionPreference = "Stop"
Write-Host "== SATN DB Seeder ==" -ForegroundColor Cyan

$seedPath = Join-Path $RepoRoot "docker\seed\seed_full.sql"
$idxPath  = Join-Path $RepoRoot "docker\init\03-indexes.sql"
if (!(Test-Path $seedPath)) { throw "Seed file not found: $seedPath" }

# Ensure container up
$running = (docker ps --filter "name=$Container" --format "{{.Names}}") -contains $Container
if (-not $running) {
  if (-not $env:POSTGRES_PASSWORD) { throw "POSTGRES_PASSWORD not set. Example: `$env:POSTGRES_PASSWORD='changeme'" }
  Write-Host "Starting compose..." -ForegroundColor Yellow
  Set-Location $RepoRoot
  docker compose -f docker\compose.yml up -d
  Start-Sleep -Seconds 4
}

# Copy + apply seed
Write-Host "Copying seed file..." -ForegroundColor Yellow
$containerSeed = "/tmp/seed_full.sql"
docker cp $seedPath "$($Container):$containerSeed"

Write-Host "Applying seed..." -ForegroundColor Yellow
docker exec -e PGPASSWORD=$env:POSTGRES_PASSWORD $Container psql -U $User -d $Db -v ON_ERROR_STOP=1 -f $containerSeed

# Apply indexes if present
if (Test-Path $idxPath) {
  Write-Host "Applying indexes..." -ForegroundColor Yellow
  $containerIdx = "/tmp/03-indexes.sql"
  docker cp $idxPath "$($Container):$containerIdx"
  docker exec -e PGPASSWORD=$env:POSTGRES_PASSWORD $Container psql -U $User -d $Db -v ON_ERROR_STOP=1 -f $containerIdx
}

# Verify counts
Write-Host "Verifying counts..." -ForegroundColor Yellow
docker exec -e PGPASSWORD=$env:POSTGRES_PASSWORD $Container psql -U $User -d $Db -c "SELECT 'agents' AS t, COUNT(*) FROM agents UNION ALL SELECT 'properties', COUNT(*) FROM properties UNION ALL SELECT 'users', COUNT(*) FROM users UNION ALL SELECT 'interactions', COUNT(*) FROM interactions ORDER BY 1;"

Write-Host "Seed complete." -ForegroundColor Green
