<# =============================================================
   SATN — Show seeded data from every table (PostgreSQL)
   Prints each table name, total row count, then top N rows.
   Picks a sensible ORDER BY (created_at/timestamp/id/title/first col).
   No psql meta-commands; just plain SELECT so output shows reliably.

   Run:
     powershell -ExecutionPolicy Bypass -File .\scripts\See_seeded_rows.ps1 -SampleRows 10
   ============================================================= #>

[CmdletBinding()]
param(
  [string]$DbContainer = "satn_pg",
  [string]$DbName      = "satn_db",
  [string]$DbUser      = "satn_admin",
  [string]$Schema      = "public",
  [int]$SampleRows     = 10
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function H1([string]$t){ Write-Host "`n=== $t ===" -ForegroundColor Cyan }
function INFO([string]$m){ Write-Host "[INFO] $m" -ForegroundColor Yellow }
function FAIL([string]$m){ Write-Host "[FAIL] $m" -ForegroundColor Red }

# Ensure password for local dev
if (-not $env:POSTGRES_PASSWORD -or [string]::IsNullOrWhiteSpace($env:POSTGRES_PASSWORD)) {
  $env:POSTGRES_PASSWORD = "changeme"
}

# psql - text output helper (unaligned, pipe-separated so wide JSON is still visible)
function Invoke-PsqlFlat([string]$Sql){
  docker exec -e PGPASSWORD=$env:POSTGRES_PASSWORD $DbContainer `
    psql -U $DbUser -d $DbName `
         -P pager=off -P null='(null)' `
         -t -A -F ' | ' `
         -c $Sql
}

# psql - regular aligned output (for the final table prints)
function Invoke-PsqlShow([string]$Sql){
  docker exec -e PGPASSWORD=$env:POSTGRES_PASSWORD $DbContainer `
    psql -U $DbUser -d $DbName `
         -P pager=off -P null='(null)' `
         -c $Sql
}

# 1) Fetch list of tables
$tableSql = "SELECT table_name
FROM information_schema.tables
WHERE table_schema = '$Schema' AND table_type = 'BASE TABLE'
ORDER BY table_name;"
$tables = Invoke-PsqlFlat $tableSql | ForEach-Object { $_.Trim() } | Where-Object { $_ }
if (-not $tables) { FAIL "No tables found in schema '$Schema'."; exit 1 }

# 2) Loop through and print data
foreach($t in $tables){
  # Count
  $cntSql = 'SELECT COUNT(*) FROM "{0}"."{1}";' -f $Schema, $t
  $cnt = (Invoke-PsqlFlat $cntSql).Trim()
  H1 ("{0}.{1} (rows: {2})" -f $Schema, $t, $cnt)

  # Prefer sensible ORDER BY column if present
  $orderPrefSql = 'WITH pref AS (SELECT unnest(ARRAY[''created_at'',''timestamp'',''id'',''title'']) AS c)
SELECT c
FROM pref
WHERE EXISTS (
  SELECT 1
  FROM information_schema.columns
  WHERE table_schema = ''{0}'' AND table_name = ''{1}'' AND column_name = c
)
LIMIT 1;' -f $Schema, $t

  $orderCol = (Invoke-PsqlFlat $orderPrefSql).Trim()

  if (-not $orderCol) {
    $firstColSql = 'SELECT column_name
FROM information_schema.columns
WHERE table_schema = ''{0}'' AND table_name = ''{1}''
ORDER BY ordinal_position
LIMIT 1;' -f $Schema, $t
    $orderCol = (Invoke-PsqlFlat $firstColSql).Trim()
  }

  # Build and run the SELECT (quote identifiers safely)
  if ($orderCol) {
    $sel = 'SELECT * FROM "{0}"."{1}" ORDER BY "{2}" NULLS LAST LIMIT {3};' -f $Schema, $t, $orderCol, $SampleRows
  } else {
    $sel = 'SELECT * FROM "{0}"."{1}" LIMIT {2};' -f $Schema, $t, $SampleRows
  }

  Invoke-PsqlShow $sel | Out-Host
}
