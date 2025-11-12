param(
  [string]$Container = "satn_pg"
)

Write-Host "== SATN: Apply DB migration ==" -ForegroundColor Cyan
if (-not $env:POSTGRES_PASSWORD) { $env:POSTGRES_PASSWORD = "changeme" }

$files = @(
  "docker/migrations/20251112_properties_attrs.sql",
  "docker/migrations/20251112_indexes.sql",
  "docker/migrations/20251112_seed_more.sql"
)

foreach ($f in $files) {
  if (!(Test-Path $f)) { throw "Missing file: $f" }
}

$running = (docker inspect -f '{{.State.Running}}' $Container 2>$null)
if ($running -ne 'true') {
  Write-Host "Starting DB container..." -ForegroundColor Yellow
  docker compose -f docker/compose.yml up -d | Out-Null
  Start-Sleep -Seconds 2
}

foreach ($f in $files) {
  $base = Split-Path $f -Leaf
  Write-Host " - Copy $base" -ForegroundColor Yellow
  docker cp $f "${Container}:/tmp/$base"
  Write-Host " - Apply $base" -ForegroundColor Yellow
  docker exec -e PGPASSWORD=$env:POSTGRES_PASSWORD $Container `
    psql -U satn_admin -d satn_db -v "ON_ERROR_STOP=1" -f "/tmp/$base"
}

Write-Host "Migration complete." -ForegroundColor Green
