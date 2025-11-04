# PowerShell Script to Set Up n8n with Persistent Volumes
# This prevents data loss when containers are restarted

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "n8n Persistent Volume Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Define paths
$n8nDataPath = Join-Path $PSScriptRoot "n8n-data"
$n8nConfigPath = Join-Path $PSScriptRoot "n8n-config"

Write-Host "Setting up persistent volumes..." -ForegroundColor Yellow
Write-Host "Data volume: $n8nDataPath" -ForegroundColor White
Write-Host "Config volume: $n8nConfigPath" -ForegroundColor White
Write-Host ""

# Create directories
New-Item -ItemType Directory -Path $n8nDataPath -Force | Out-Null
New-Item -ItemType Directory -Path $n8nConfigPath -Force | Out-Null

Write-Host "Created directories" -ForegroundColor Green

# Stop current n8n container
Write-Host ""
Write-Host "Stopping current n8n container..." -ForegroundColor Yellow
docker stop n8n 2>$null

# Remove current container (but keep the image)
Write-Host "Removing old container..." -ForegroundColor Yellow
docker rm n8n 2>$null

# Start new container with persistent volumes
Write-Host ""
Write-Host "Starting n8n with persistent volumes..." -ForegroundColor Yellow
Write-Host ""

# Convert Windows paths to Docker-compatible paths
$n8nDataPathDocker = $n8nDataPath -replace '\\', '/' -replace 'C:', '/c'
$n8nConfigPathDocker = $n8nConfigPath -replace '\\', '/' -replace 'C:', '/c'

docker run -d `
  --name n8n `
  --hostname n8n-persistent `
  -p 5678:5678 `
  -v "${n8nDataPathDocker}:/home/node/.n8n" `
  -v "${n8nConfigPathDocker}:/home/node/.n8n-config" `
  -e WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev `
  --restart always `
  n8nio/n8n:latest

Write-Host ""
Write-Host "Waiting for n8n to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if container is running
$containerStatus = docker ps --filter "name=n8n" --format "{{.Status}}"
if ($containerStatus -match "Up") {
    Write-Host "✅ n8n started successfully with persistent volumes!" -ForegroundColor Green
} else {
    Write-Host "❌ n8n failed to start" -ForegroundColor Red
    docker logs n8n
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Persistent Volume Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your n8n data is now persistent:" -ForegroundColor Cyan
Write-Host "📁 Data: $n8nDataPath" -ForegroundColor White
Write-Host "⚙️  Config: $n8nConfigPath" -ForegroundColor White
Write-Host ""
Write-Host "Benefits:" -ForegroundColor Cyan
Write-Host "✅ Workflows persist across container restarts" -ForegroundColor White
Write-Host "✅ Credentials persist across container restarts" -ForegroundColor White
Write-Host "✅ Execution history is preserved" -ForegroundColor White
Write-Host "✅ No more data loss!" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Open http://localhost:5678 to access n8n" -ForegroundColor White
Write-Host "2. Import your workflows using import_workflows.py" -ForegroundColor White
Write-Host "3. Reconfigure credentials" -ForegroundColor White
Write-Host "4. Run backup_n8n.ps1 regularly to create snapshots" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue"