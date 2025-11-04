# PowerShell Script to Restart n8n Docker with HTTPS Webhook Support
# Run this on the Windows 11 machine at 192.168.0.14

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "n8n Docker - HTTPS Webhook Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Stopping current n8n container..." -ForegroundColor Yellow
docker stop n8n 2>$null

Write-Host "Step 2: Removing old container..." -ForegroundColor Yellow
docker rm n8n 2>$null

Write-Host "Step 3: Starting new container with HTTPS webhook..." -ForegroundColor Yellow
Write-Host ""

docker run `
  --hostname=5cbd5e6e12a6 `
  --user=node `
  --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin `
  --env=NODE_VERSION=22.18.0 `
  --env=YARN_VERSION=1.22.22 `
  --env=NODE_ICU_DATA=/usr/local/lib/node_modules/full-icu `
  --env=NODE_ENV=production `
  --env=N8N_RELEASE_TYPE=stable `
  --env=SHELL=/bin/sh `
  --env=WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev `
  --network=bridge `
  --workdir=/home/node `
  -p 5678:5678 `
  --restart=always `
  --name=n8n `
  --label='org.opencontainers.image.description=Workflow Automation Tool' `
  --label='org.opencontainers.image.source=https://github.com/n8n-io/n8n' `
  --label='org.opencontainers.image.title=n8n' `
  --label='org.opencontainers.image.url=https://n8n.io' `
  --label='org.opencontainers.image.version=1.117.3' `
  --runtime=runc `
  -d `
  n8nio/n8n:latest

Write-Host ""
Write-Host "Waiting 5 seconds for n8n to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Step 4: Checking container status..." -ForegroundColor Yellow
docker ps | Select-String "n8n"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "DONE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Open http://192.168.0.14:5678" -ForegroundColor White
Write-Host "2. Go to Workflows > AIPA - Telegram Main Interface" -ForegroundColor White
Write-Host "3. Click the Telegram Trigger node" -ForegroundColor White
Write-Host "4. Verify webhook URL shows HTTPS" -ForegroundColor White
Write-Host "5. Activate the workflow" -ForegroundColor White
Write-Host "6. Send /start to your Telegram bot" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
