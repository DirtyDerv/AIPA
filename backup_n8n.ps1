# n8n Backup Script for PowerShell
# Creates timestamped backups of workflows and credentials

param(
    [switch]$Auto
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "n8n Backup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $PSScriptRoot "backups\n8n_backup_$timestamp"

Write-Host "Creating backup directory: $backupDir" -ForegroundColor Yellow
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

Write-Host ""
Write-Host "[1/3] Backing up workflows..." -ForegroundColor Yellow

# Python script to backup workflows
$pythonScript = @'
import requests
import json
import os
from datetime import datetime

url = "http://localhost:5678/api/v1/workflows"
headers = {
    "X-N8N-API-KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"
}

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        workflows = response.json().get("data", [])
        print(f"Found {len(workflows)} workflows")
        
        for wf in workflows:
            filename = f"{wf['id']}_{wf['name'].replace(' ', '_').replace('/', '_')}.json"
            filepath = os.path.join(r"'.$backupDir.'", "workflows", filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(wf, f, indent=2, ensure_ascii=False)
        
        print("Workflows backed up successfully")
    else:
        print(f"Failed to backup workflows: {response.status_code}")
except Exception as e:
    print(f"Error backing up workflows: {e}")
'@

# Execute Python script
$pythonScript | python | Tee-Object -FilePath "$backupDir\workflow_backup.log"

Write-Host ""
Write-Host "[2/3] Backing up workflow JSON files..." -ForegroundColor Yellow

# Copy workflow files
$workflowSource = Join-Path $PSScriptRoot "n8n-workflows"
if (Test-Path $workflowSource) {
    $workflowDest = Join-Path $backupDir "workflow_files"
    New-Item -ItemType Directory -Path $workflowDest -Force | Out-Null
    
    Copy-Item "$workflowSource\*.json" $workflowDest -ErrorAction SilentlyContinue
    Write-Host "Copied workflow files" -ForegroundColor Green
} else {
    Write-Host "No workflow files found in n8n-workflows\" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[3/3] Creating backup manifest..." -ForegroundColor Yellow

# Create backup info
$backupInfo = @"
n8n Backup Created: $timestamp

This backup contains:
- Exported workflow definitions from n8n API
- Local workflow JSON files

To restore:
1. Use import_workflows.py to import workflow_files/*.json
2. Manually reconfigure credentials in n8n web interface
3. Activate workflows as needed

IMPORTANT: Credentials are NOT backed up for security reasons.
Document your credential setup process separately.
"@

$backupInfo | Out-File -FilePath "$backupDir\BACKUP_INFO.txt" -Encoding UTF8

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Backup Complete!" -ForegroundColor Green
Write-Host "Location: $backupDir" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

if (-not $Auto) {
    Write-Host ""
    Write-Host "Next steps for disaster recovery:" -ForegroundColor Cyan
    Write-Host "1. Keep this backup folder safe" -ForegroundColor White
    Write-Host "2. Consider setting up automated backups" -ForegroundColor White
    Write-Host "3. Document your credential setup process" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to continue"
}