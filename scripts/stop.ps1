
# Kill any processes on ports 3000 and 8001
Get-NetTCPConnection -LocalPort 3000, 8001 -ErrorAction SilentlyContinue | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
}

Write-Host "Stopped servers on ports 3000 and 8001"
