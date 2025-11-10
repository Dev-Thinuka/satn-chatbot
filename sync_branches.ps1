    # ===========================================
    # SA Thomson Nerys Chatbot - Git Sync Assistant (Interactive)
    # Branch flow: dev → main → backup-local
    # ===========================================

    function Confirm-Step($message) {
        $response = Read-Host "$message (y/n)"
        if ($response -ne 'y') {
            Write-Host "❌ Step skipped. Exiting..." -ForegroundColor Red
            exit
        }
    }

    Write-Host "`n🚀 Starting SA Thomson Nerys Git Sync Wizard..." -ForegroundColor Cyan

    # Check current branch
    $currentBranch = git rev-parse --abbrev-ref HEAD
    Write-Host "`n📍 You are currently on branch: $currentBranch" -ForegroundColor Yellow

    Confirm-Step "Continue with synchronization process?"

    # Auto commit pending changes
    Write-Host "`n📦 Checking for uncommitted changes..." -ForegroundColor Cyan
    $changes = git status --porcelain
    if ($changes) {
        git add .
        git commit -m "chore(sync): auto-commit before sync"
        Write-Host "✅ Local changes committed." -ForegroundColor Green
    } else {
        Write-Host "ℹ️ No changes to commit." -ForegroundColor DarkGray
    }

    # Step 1: Merge dev → main
    Confirm-Step "Proceed to merge dev → main?"
    git checkout main
    git pull origin main
    git merge dev

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Merge successful. Pushing main to remote..." -ForegroundColor Green
        git push origin main
    } else {
        Write-Host "⚠️ Merge conflict detected in main. Resolve manually and rerun script." -ForegroundColor Red
        exit 1
    }

    # Step 2: Merge main → backup-local
    Confirm-Step "Proceed to merge main → backup-local?"
    git checkout backup-local
    git pull origin backup-local
    git merge main

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Backup branch updated. Pushing backup-local to remote..." -ForegroundColor Green
        git push origin backup-local
    } else {
        Write-Host "⚠️ Merge conflict in backup-local. Resolve manually." -ForegroundColor Red
        exit 1
    }

    # Step 3: Return to dev branch
    git checkout dev
    Write-Host "`n🎉 All branches synchronized successfully!" -ForegroundColor Green

    # Summary
    Write-Host "`n================= SYNC SUMMARY =================" -ForegroundColor Cyan
    Write-Host "• dev branch merged into → main" -ForegroundColor White
    Write-Host "• main branch merged into → backup-local" -ForegroundColor White
    Write-Host "• backup-local and main both pushed to origin ✅" -ForegroundColor Green
    Write-Host "================================================`n" -ForegroundColor Cyan
