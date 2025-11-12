Param(
  [string]$Container = "satn_pg",
  [string]$Db = "satn_db",
  [string]$User = "satn_admin"
)

$check = @"
SELECT 'agents' AS table, COUNT(*) FROM agents
UNION ALL SELECT 'properties', COUNT(*) FROM properties
UNION ALL SELECT 'users', COUNT(*) FROM users
UNION ALL SELECT 'interactions', COUNT(*) FROM interactions
ORDER BY table;
"@

docker exec -i $Container psql -U $User -d $Db -c "$check"

# Sample read (Sydney filter)
$sample = "SELECT title, location, price FROM properties WHERE location ILIKE '%Sydney%' OR title ILIKE '%Sydney%';"
docker exec -i $Container psql -U $User -d $Db -c "$sample"


#powershell -ExecutionPolicy Bypass -File scripts\db_check.ps1
