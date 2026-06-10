
# Kill any existing processes on ports 3000 and 8001
Get-NetTCPConnection -LocalPort 3000, 8001 -ErrorAction SilentlyContinue | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
}

# Start the backend server
Start-Process -FilePath "uv" -ArgumentList "run", "python", "main.py" -WorkingDirectory "server" -WindowStyle Minimized

# Start the frontend server
Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory "client" -WindowStyle Minimized

Write-Host "Servers started:"
Write-Host "Backend: http://localhost:8001"
Write-Host "Frontend: http://localhost:3000"
