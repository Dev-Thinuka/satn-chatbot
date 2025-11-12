Param(
  [string]$FrontendPath = "C:\Repositories\sa-thomson-chatbot\frontend"
)

Write-Host "== SATN Frontend reset ==" -ForegroundColor Cyan
Set-Location $FrontendPath

# Clean prior tooling (tailwind/postcss remnants)
@("node_modules", "package-lock.json", ".vite", "dist") | ForEach-Object {
  if (Test-Path $_) { Remove-Item -Recurse -Force $_ }
}

# Fresh install (only 'serve')
npm install

Write-Host "Starting static server on http://localhost:5173 ..." -ForegroundColor Green
npm run start
