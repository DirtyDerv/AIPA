@echo off
REM n8n Webhook Configuration Script for Windows
REM Run this on the Windows machine where n8n is running

echo ========================================
echo n8n Webhook HTTPS Configuration
echo ========================================
echo.

REM Set the webhook URL
set WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev

echo [OK] Webhook URL set to: %WEBHOOK_URL%
echo.

REM Check if n8n is running
tasklist /FI "IMAGENAME eq node.exe" 2>NUL | find /I /N "node.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [WARN] Node.js processes are running
    echo We'll start n8n with the new configuration...
    echo.
)

REM Set environment variable permanently for current user
setx WEBHOOK_URL "https://uniterative-futile-charmain.ngrok-free.dev"

echo [OK] WEBHOOK_URL saved to environment variables
echo.
echo ========================================
echo Starting n8n...
echo ========================================
echo.

REM Start n8n with the webhook URL
start "n8n" cmd /k "set WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev && n8n start"

timeout /t 5 /nobreak > NUL

echo.
echo ========================================
echo DONE!
echo ========================================
echo.
echo Next steps:
echo 1. Check the n8n window that just opened
echo 2. Open http://192.168.0.14:5678 in your browser
echo 3. Open 'AIPA - Telegram Main Interface' workflow
echo 4. Click on the 'Telegram Trigger' node
echo 5. Verify the webhook URL shows HTTPS
echo 6. Activate the workflow
echo 7. Test by sending /start to your Telegram bot
echo.
pause
