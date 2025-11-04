# 🚀 AIPA Discord Bot - 24/7 Deployment Guide

## 🎯 Quick Start (Recommended)

### Option 1: Automatic Setup (Easiest)
```powershell
# Run as Administrator
.\setup_bot_scheduler.ps1
```
This creates a Windows Task Scheduler task that starts the bot automatically at Windows startup and user login.

### Option 2: Manual Background Start
```powershell
# Start the bot
.\run_discord_bot.ps1

# Check status
.\run_discord_bot.ps1 -Status

# Stop the bot
.\run_discord_bot.ps1 -Stop

# Restart the bot
.\run_discord_bot.ps1 -Restart
```

### Option 3: Simple Batch File
```batch
# Double-click this file to start the bot in background
start_discord_bot.bat
```

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `run_discord_bot.ps1` | Main control script (start/stop/status/restart) |
| `setup_bot_scheduler.ps1` | **Run as Admin** - Sets up automatic startup |
| `start_discord_bot.bat` | Simple batch file for manual starting |
| `monitor_bot.ps1` | Monitors bot health and auto-restarts if needed |
| `AIPA_Discord_Bot_Task.xml` | Task Scheduler XML (alternative import method) |

---

## 🔧 Manual Task Scheduler Setup

If the automatic setup doesn't work:

1. **Open Task Scheduler**: Press `Win + R`, type `taskschd.msc`
2. **Create New Task**:
   - Name: `AIPA Discord Bot`
   - Run with highest privileges: ✅
   - Configure for: Windows 10
3. **Triggers Tab**:
   - At log on (any user)
   - At startup
4. **Actions Tab**:
   - Action: Start a program
   - Program: `powershell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File "C:\Users\woody\OneDrive\Documents\AI\AIPA\run_discord_bot.ps1"`
   - Start in: `C:\Users\woody\OneDrive\Documents\AI\AIPA`
5. **Conditions Tab**:
   - Start only if network is available: ✅
6. **Save and test**

---

## 📊 Monitoring & Management

### Check Bot Status
```powershell
.\run_discord_bot.ps1 -Status
```

### Start Monitoring Service
```powershell
# Monitor every 5 minutes (default)
.\monitor_bot.ps1

# Monitor every 10 minutes
.\monitor_bot.ps1 -CheckInterval 600

# Single check only
.\monitor_bot.ps1 -Once
```

### View Logs
- Bot logs: `discord_bot.log`
- Monitor logs: `bot_monitor.log`

---

## 🔍 Troubleshooting

### Bot Won't Start
1. Check Python installation: `python --version`
2. Install dependencies: `pip install discord.py`
3. Check bot token in `discord_bot_bmf.py`
4. Run manually first: `python bot\discord_bot_bmf.py`

### Task Scheduler Issues
1. Run setup script as Administrator
2. Check Task Scheduler for error messages
3. Verify PowerShell execution policy: `Get-ExecutionPolicy`
4. Try importing XML: `schtasks /create /tn "AIPA Discord Bot" /xml "AIPA_Discord_Bot_Task.xml"`

### Permission Issues
- Make sure you're running scripts from the AIPA directory
- Check file permissions on bot files
- Run PowerShell as Administrator for setup

---

## 🎯 What's Running in Background

- **pythonw.exe**: The actual bot process (no visible window)
- **PID file**: `discord_bot.pid` tracks the process ID
- **Task Scheduler**: Monitors and restarts on Windows events
- **Monitor script**: Optional health checking service

---

## 🛑 Emergency Stop

If you need to force stop everything:
```powershell
# Stop bot
.\run_discord_bot.ps1 -Stop

# Kill any remaining python processes
Get-Process python* | Stop-Process -Force

# Remove from Task Scheduler
schtasks /delete /tn "AIPA Discord Bot"
```

---

## ✅ Success Indicators

- **Task Manager**: Look for `pythonw.exe` process
- **Discord**: Bot shows as online in your server
- **Logs**: Check `discord_bot.log` for "Bot started successfully"
- **Status command**: `.\run_discord_bot.ps1 -Status` shows "Running"

---

## 🚀 Advanced Configuration

### Virtual Environment
The scripts automatically detect and use `.venv` if it exists.

### Custom Log Location
Edit the scripts to change `$LogFile` path.

### Multiple Instances
Modify scripts to support multiple bot instances.

---

**🎉 Your Discord bot will now run 24/7! Test it by sending a message in your Discord server.**