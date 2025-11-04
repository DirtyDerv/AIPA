# AIPA Discord Bot Monitor
# This script checks if the bot is running and restarts it if needed

param(
    [int]$CheckInterval = 300,  # 5 minutes default
    [switch]$Once  # Run check once instead of continuously
)

$BotPath = "C:\Users\woody\OneDrive\Documents\AI\AIPA"
$BotScript = "$BotPath\run_discord_bot.ps1"
$LogFile = "$BotPath\bot_monitor.log"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -FilePath $LogFile -Append
    Write-Host "[$timestamp] $Message"
}

function Test-BotRunning {
    $process = Get-Process | Where-Object {
        $_.ProcessName -eq "pythonw" -and
        $_.CommandLine -like "*discord_bot_bmf.py*"
    }
    return $null -ne $process
}

function Restart-Bot {
    Write-Log "Bot not running, attempting to restart..."
    try {
        & $BotScript
        Start-Sleep -Seconds 5
        if (Test-BotRunning) {
            Write-Log "Bot restarted successfully"
        } else {
            Write-Log "Failed to restart bot"
        }
    }
    catch {
        Write-Log "Error restarting bot: $($_.Exception.Message)"
    }
}

Write-Log "AIPA Discord Bot Monitor started"
Write-Log "Check interval: $CheckInterval seconds"

if ($Once) {
    Write-Log "Running single check..."
    if (-not (Test-BotRunning)) {
        Write-Log "Bot is not running"
        Restart-Bot
    } else {
        Write-Log "Bot is running normally"
    }
    exit
}

# Continuous monitoring loop
Write-Log "Starting continuous monitoring..."
while ($true) {
    if (-not (Test-BotRunning)) {
        Write-Log "Bot process not found"
        Restart-Bot
    }

    # Brief status check every interval
    if ((Get-Date).Minute % 30 -eq 0) {  # Log status every 30 minutes
        if (Test-BotRunning) {
            Write-Log "Bot status check: Running"
        }
    }

    Start-Sleep -Seconds $CheckInterval
}