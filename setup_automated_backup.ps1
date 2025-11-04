# PowerShell Script to Set Up Automated n8n Backups
# Creates a Windows Scheduled Task for daily backups

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Automated n8n Backup Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ This script requires administrator privileges" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Define paths
$scriptPath = Join-Path $PSScriptRoot "backup_n8n.ps1"
$taskName = "AIPA n8n Daily Backup"

Write-Host "Setting up automated backup..." -ForegroundColor Yellow
Write-Host "Script: $scriptPath" -ForegroundColor White
Write-Host "Task Name: $taskName" -ForegroundColor White
Write-Host ""

# Check if backup script exists
if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ Backup script not found: $scriptPath" -ForegroundColor Red
    Write-Host "Please run this script from the AIPA directory" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Remove existing task if it exists
Write-Host "Removing existing backup task (if any)..." -ForegroundColor Yellow
schtasks /delete /tn "$taskName" /f 2>$null

# Create new scheduled task (runs daily at 2 AM)
Write-Host "Creating daily backup task..." -ForegroundColor Yellow
$taskCommand = "powershell.exe -ExecutionPolicy Bypass -File `"$scriptPath`" -Auto"

schtasks /create /tn "$taskName" /tr "$taskCommand" /sc daily /st 02:00 /ru "$env:USERNAME" /rl highest /f

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Automated backup task created successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create backup task" -ForegroundColor Red
    Write-Host "You can manually run backup_n8n.ps1 instead" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Test the task
Write-Host ""
Write-Host "Testing backup task..." -ForegroundColor Yellow
schtasks /run /tn "$taskName"
Start-Sleep -Seconds 5

# Check if backup was created
$backupDir = Join-Path $PSScriptRoot "backups"
if (Test-Path $backupDir) {
    $latestBackup = Get-ChildItem $backupDir -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestBackup) {
        Write-Host "✅ Test backup created: $($latestBackup.Name)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Automated Backup Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backup Schedule:" -ForegroundColor Cyan
Write-Host "📅 Daily at 2:00 AM" -ForegroundColor White
Write-Host "📁 Location: .\backups\" -ForegroundColor White
Write-Host "🔧 Task Name: $taskName" -ForegroundColor White
Write-Host ""
Write-Host "To manage the backup task:" -ForegroundColor Cyan
Write-Host "1. Open Task Scheduler (taskschd.msc)" -ForegroundColor White
Write-Host "2. Navigate to Task Scheduler Library" -ForegroundColor White
Write-Host "3. Find '$taskName'" -ForegroundColor White
Write-Host "4. Right-click to modify schedule or disable" -ForegroundColor White
Write-Host ""
Write-Host "Manual backup options:" -ForegroundColor Cyan
Write-Host "• Run .\backup_n8n.ps1 for immediate backup" -ForegroundColor White
Write-Host "• Run .\backup_n8n.bat for batch file backup" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue"