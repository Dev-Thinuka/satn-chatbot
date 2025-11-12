<#
.SYNOPSIS
  Lists the full folder and file structure of the backend directory
  and saves it to a text file.
#>

# --- Configuration ---
$backendPath = "C:\Repositories\sa-thomson-chatbot\backend"
$outputFile = Join-Path $backendPath "backend_structure.txt"

Write-Host "Scanning backend folder: $backendPath`n"

# Remove old file if it exists
if (Test-Path $outputFile) { Remove-Item $outputFile }

# --- Recursive tree listing ---
function Show-Tree {
    param (
        [string]$Path,
        [string]$Indent = ""
    )

    # List directories
    $dirs = Get-ChildItem -Path $Path -Directory -Force | Sort-Object Name
    foreach ($dir in $dirs) {
        $line = "$Indent[D] $($dir.Name)"
        Write-Output $line | Tee-Object -FilePath $outputFile -Append
        Show-Tree -Path $dir.FullName -Indent ("$Indent    ")
    }

    # List files
    $files = Get-ChildItem -Path $Path -File -Force | Sort-Object Name
    foreach ($file in $files) {
        $line = "$Indent[F] $($file.Name)"
        Write-Output $line | Tee-Object -FilePath $outputFile -Append
    }
}

# --- Start scanning ---
Show-Tree -Path $backendPath

Write-Host "`nFile structure saved to: $outputFile"
