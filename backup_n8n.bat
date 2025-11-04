@echo off
REM n8n Backup Script for Windows
REM Creates timestamped backups of workflows and credentials

echo ========================================
echo n8n Backup Script
echo ========================================
echo.

set TIMESTAMP=%date:~-4,4%%date:~-10,4%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_DIR=%~dp0backups\n8n_backup_%TIMESTAMP%

echo Creating backup directory: %BACKUP_DIR%
mkdir "%BACKUP_DIR%" 2>nul

echo.
echo [1/3] Backing up workflows...
python -c "
import requests
import json
import os
from datetime import datetime

url = 'http://localhost:5678/api/v1/workflows'
headers = {
    'X-N8N-API-KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk'
}

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        workflows = response.json().get('data', [])
        print(f'Found {len(workflows)} workflows')
        
        for wf in workflows:
            filename = f'{wf[\"id\"]}_{wf[\"name\"].replace(\" \", \"_\").replace(\"/\", \"_\")}.json'
            filepath = os.path.join(r'%BACKUP_DIR%', 'workflows', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(wf, f, indent=2, ensure_ascii=False)
        
        print('Workflows backed up successfully')
    else:
        print(f'Failed to backup workflows: {response.status_code}')
except Exception as e:
    print(f'Error backing up workflows: {e}')
" > "%BACKUP_DIR%\workflow_backup.log" 2>&1

echo.
echo [2/3] Backing up workflow JSON files...
if exist "n8n-workflows\*.json" (
    mkdir "%BACKUP_DIR%\workflow_files" 2>nul
    copy "n8n-workflows\*.json" "%BACKUP_DIR%\workflow_files\" >nul
    echo Copied workflow files
) else (
    echo No workflow files found in n8n-workflows\
)

echo.
echo [3/3] Creating backup manifest...
echo n8n Backup Created: %TIMESTAMP% > "%BACKUP_DIR%\BACKUP_INFO.txt"
echo. >> "%BACKUP_DIR%\BACKUP_INFO.txt"
echo This backup contains: >> "%BACKUP_DIR%\BACKUP_INFO.txt"
echo - Exported workflow definitions from n8n API >> "%BACKUP_DIR%\BACKUP_INFO.txt"
echo - Local workflow JSON files >> "%BACKUP_DIR%\BACKUP_INFO.txt"
echo. >> "%BACKUP_DIR%\BACKUP_INFO.txt"
echo To restore: >> "%BACKUP_DIR%\BACKUP_INFO.txt"
echo 1. Use import_workflows.py to import workflow_files/*.json >> "%BACKUP_DIR%\BACKUP_INFO.txt"
echo 2. Manually reconfigure credentials in n8n web interface >> "%BACKUP_DIR%\BACKUP_INFO.txt"
echo 3. Activate workflows as needed >> "%BACKUP_DIR%\BACKUP_INFO.txt"

echo.
echo ========================================
echo Backup Complete!
echo Location: %BACKUP_DIR%
echo ========================================
echo.
echo Next steps for disaster recovery:
echo 1. Keep this backup folder safe
echo 2. Consider setting up automated backups
echo 3. Document your credential setup process
echo.
pause