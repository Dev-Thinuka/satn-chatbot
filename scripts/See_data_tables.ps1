# ==== SATN: Show all tables (public) with their columns ====
# Requires Docker and your satn_pg container running.

# 0) Defaults (edit if needed)
$DbContainer = "satn_pg"
$DbName      = "satn_db"
$DbUser      = "satn_admin"
$Schema      = "public"

# 1) Ensure password for local dev
if (-not $env:POSTGRES_PASSWORD -or [string]::IsNullOrWhiteSpace($env:POSTGRES_PASSWORD)) {
  $env:POSTGRES_PASSWORD = "changeme"
}

# 2) Helper to run psql with tidy output
function Invoke-Psql([string]$Sql){
  docker exec -e PGPASSWORD=$env:POSTGRES_PASSWORD $DbContainer `
    psql -U $DbUser -d $DbName -P pager=off -t -A -c $Sql
}

# 3) Get list of tables in the schema
$tablesSql = @"
SELECT table_name
FROM information_schema.tables
WHERE table_schema = '$Schema' AND table_type = 'BASE TABLE'
ORDER BY table_name;
"@
$tables = Invoke-Psql $tablesSql | ForEach-Object { $_.Trim() } | Where-Object { $_ }

if (-not $tables) {
  Write-Host "No tables found in schema '$Schema'." -ForegroundColor Yellow
  return
}

# 4) Print each table with its columns
foreach($t in $tables) {
  Write-Host "`n=== $Schema.$t ===" -ForegroundColor Cyan

  $colsSql = @"
SELECT
  c.ordinal_position      AS pos,
  c.column_name           AS name,
  c.data_type             AS type,
  COALESCE(c.character_maximum_length::text, '') AS len,
  c.is_nullable           AS nullable,
  COALESCE(c.column_default,'') AS default
FROM information_schema.columns c
WHERE c.table_schema = '$Schema'
  AND c.table_name   = '$t'
ORDER BY c.ordinal_position;
"@

  # Show columns
  docker exec -e PGPASSWORD=$env:POSTGRES_PASSWORD $DbContainer `
    psql -U $DbUser -d $DbName -P pager=off -c $colsSql

  # Optional: show row count (uncomment if you want row counts)
  # $cnt = Invoke-Psql "SELECT COUNT(*) FROM `"$Schema`"."$t`";"
  # Write-Host ("Rows: {0}" -f $cnt.Trim())
}
