# Create one git worktree per lab, up front. Safe to re-run: skips any that already exist.
# Each lab gets ..\lab-N-work on a new branch lab-N-work, created from origin/lab-N-start.
# Run from your clone of the fork:  .\scripts\setup-worktrees.ps1
$ErrorActionPreference = "Stop"

Write-Host "Fetching latest branches..."
git fetch origin --quiet

$created = 0
$skipped = 0
$worktrees = (git worktree list)
foreach ($n in 1..9) {
    $dir    = "..\lab-$n-work"
    $branch = "lab-$n-work"
    if ($worktrees -match "lab-$n-work") {
        Write-Host "  lab-$n: already set up, skipping"
        $skipped++
        continue
    }
    git show-ref --verify --quiet "refs/heads/$branch"
    if ($LASTEXITCODE -eq 0) {
        git worktree add $dir $branch
        Write-Host "  lab-$n: worktree created (existing branch)"
    } else {
        git worktree add -b $branch $dir "origin/lab-$n-start"
        Write-Host "  lab-$n: worktree + branch created from origin/lab-$n-start"
    }
    $created++
}

Write-Host ""
Write-Host "Done: $created created, $skipped already present."
Write-Host "Start a lab with:  cd ..\lab-1-work   (then open a fresh Claude Code session there)"
