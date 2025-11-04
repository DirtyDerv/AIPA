# AIPA Discord Bot - Windows Task Scheduler Setup
# Run this script as Administrator to set up automatic bot startup

Write-Host "🤖 AIPA Discord Bot - Windows Task Scheduler Setup" -ForegroundColor Cyan
Write-Host "=" * 55

# Check if running as administrator
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$adminRole = [Security.Principal.WindowsBuiltInRole]::Administrator

if (-not $principal.IsInRole($adminRole)) {
    Write-Host "❌ This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "💡 Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

$TaskName = "AIPA Discord Bot"
$TaskPath = "C:\Users\woody\OneDrive\Documents\AI\AIPA"
$ScriptPath = "$TaskPath\run_discord_bot.ps1"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "⚠️  Task '$TaskName' already exists!" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (y/n)"
    if ($overwrite -ne 'y') {
        Write-Host "Setup cancelled." -ForegroundColor Gray
        exit 0
    }
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create the scheduled task
Write-Host "📝 Creating scheduled task..." -ForegroundColor White

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$ScriptPath`"" -WorkingDirectory $TaskPath
$trigger1 = New-ScheduledTaskTrigger -AtLogon -User "woody"
$trigger2 = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable -ExecutionTimeLimit 0
$principal = New-ScheduledTaskPrincipal -UserId "woody" -LogonType InteractiveToken -RunLevel LeastPrivilege

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger1, $trigger2 -Settings $settings -Principal $principal -Description "Starts the AIPA Discord Bot automatically when Windows starts or user logs on"

Write-Host "✅ Task created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Task Details:" -ForegroundColor Cyan
Write-Host "   Name: $TaskName"
Write-Host "   Triggers: At startup + At logon"
Write-Host "   Action: Run PowerShell script"
Write-Host ""
Write-Host "🚀 The bot will now start automatically when:"
Write-Host "   • Windows starts up"
Write-Host "   • You log on to your account"
Write-Host ""
Write-Host "📊 To manage the task:" -ForegroundColor White
Write-Host "   • Open Task Scheduler (taskschd.msc)"
Write-Host "   • Navigate to Task Scheduler Library"
Write-Host "   • Find '$TaskName'"
Write-Host ""
Write-Host "🔧 Manual control commands:" -ForegroundColor White
Write-Host "   • Start: .\run_discord_bot.ps1"
Write-Host "   • Stop: .\run_discord_bot.ps1 -Stop"
Write-Host "   • Status: .\run_discord_bot.ps1 -Status"
Write-Host "   • Restart: .\run_discord_bot.ps1 -Restart"
Write-Host ""
Write-Host "🎉 Setup complete! The bot will run 24/7 in the background." -ForegroundColor Green