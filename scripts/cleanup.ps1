Param(
    [switch]$Execute = $false
)
# Clean working tree based on decision to drop ETL/WordPress syncing.
# DRY-RUN by default. Use -Execute to actually delete.

$Root = "C:\Repositories\sa-thomson-chatbot"

$deletePaths = @(
    # Python/Node caches & envs
    "**\__pycache__",
    "**\.pytest_cache",
    "**\.mypy_cache",
    "**\.ruff_cache",
    "**\node_modules",
    "**\.venv",
    "**\.env",               # ensure real secrets are rotated and excluded
    "**\.env.local",
    # ETL / WordPress sync / Airbyte / notebooks
    "etl\**",
    "data\raw\**",
    "data\staging\**",
    "airbyte\**",
    "dags\**",
    "scripts\etl\**",
    "notebooks\**",
    # Media & misc
    "assets\screenshots\**",
    "uploads\**",
    # Container stacks we are not using
    "docker\airbyte\**",
    "docker\kafka\**"
)

$resolved = @()
foreach ($pattern in $deletePaths) {
    $items = Get-ChildItem -Path (Join-Path $Root $pattern) -Recurse -Force -ErrorAction SilentlyContinue
    $resolved += $items
}

$resolved = $resolved | Sort-Object -Property FullName -Unique

Write-Host "=== CLEANUP PLAN ==="
$resolved | ForEach-Object { Write-Host $_.FullName }

if ($Execute) {
    Write-Host "`nDeleting..." -ForegroundColor Yellow
    foreach ($i in $resolved) {
        try {
            if (Test-Path $i.FullName) {
                Remove-Item $i.FullName -Recurse -Force -ErrorAction Stop
            }
        } catch {
            Write-Warning "Failed to remove $($i.FullName): $($_.Exception.Message)"
        }
    }
    Write-Host "Done."
} else {
    Write-Host "`nDRY RUN complete. Re-run with -Execute to delete."
}

# Git hygiene (optional): remove untracked files safely
# cd $Root; git clean -xdf -n   # dry-run
# cd $Root; git clean -xdf      # execute (be careful)
