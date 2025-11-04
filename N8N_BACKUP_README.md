# n8n Backup & Recovery System

## 🚨 Problem Solved

Your n8n workflows and credentials were lost because the Docker container wasn't using persistent volumes. All data was stored inside the container and disappeared when it was restarted.

## ✅ Solutions Implemented

### 1. **Immediate Backup Scripts**
- `backup_n8n.ps1` - PowerShell backup script (recommended)
- `backup_n8n.bat` - Batch file backup script

### 2. **Persistent Volume Setup**
- `setup_n8n_persistent.ps1` - Sets up n8n with persistent Docker volumes
- Prevents future data loss by storing data outside the container

### 3. **Automated Backups**
- `setup_automated_backup.ps1` - Creates Windows Scheduled Task for daily backups
- Runs automatically at 2:00 AM every day

## 📁 What Gets Backed Up

### ✅ Included in Backup:
- **Workflow Definitions** - Complete workflow JSON from n8n API
- **Workflow Files** - Your local `n8n-workflows/*.json` files
- **Backup Manifest** - Instructions for restoration

### ❌ NOT Included (Security):
- **Credentials** - API keys, passwords, tokens
- **Execution History** - Past workflow runs
- **User Sessions** - Login data

## 🔐 Credential Management

**Credentials are NOT automatically backed up** for security reasons, but you have tools to manage them:

### Option 1: Document Credentials (Recommended)
```powershell
.\document_credentials.ps1
```
Creates a secure reference document with all your credential information.

### Option 2: Manual Documentation
Keep your credentials documented in:
- `config/CREDENTIALS.md` ✅ (Already exists)
- `docs/CREDENTIAL_SETUP_GUIDE.md` ✅ (Already exists)

### Option 3: Password Manager
Store credentials in a secure password manager like:
- Bitwarden, LastPass, or 1Password
- Keep master credentials list for n8n setup

## 🚀 Quick Start

### Step 1: Set Up Persistent Volumes (Prevents Future Loss)
```powershell
.\setup_n8n_persistent.ps1
```

### Step 2: Create Your First Backup
```powershell
.\backup_n8n.ps1
```

### Step 3: Set Up Automated Backups (Optional)
```powershell
.\setup_automated_backup.ps1  # Requires Administrator
```

## 📂 Backup Structure

```
backups/
└── n8n_backup_20251103_140000/
    ├── workflows/           # API-exported workflows
    │   ├── abc123_Workflow_Name.json
    │   └── def456_Another_Workflow.json
    ├── workflow_files/      # Local JSON files
    │   ├── 01-telegram-main-interface.json
    │   └── 02-email-processing-ai.json
    ├── workflow_backup.log  # Backup log
    └── BACKUP_INFO.txt      # Recovery instructions
```

## 🔄 Recovery Process

If you lose n8n data again:

### Option A: Quick Restore (if using persistent volumes)
1. n8n data is automatically preserved - just restart the container

### Option B: Full Restore from Backup
1. **Import Workflows:**
   ```bash
   python tools/import_workflows.py
   ```
2. **Reconfigure Credentials** (see `docs/CREDENTIAL_SETUP_GUIDE.md`)
3. **Activate Workflows** in n8n web interface

## 📋 Credential Recovery Checklist

After restoring workflows, reconfigure these credentials in n8n:

- [ ] **Telegram Bot API** - `8266056282:AAHhTaM_1sRI5ekjnCHuBjlKmRvbKQQTEhI`
- [ ] **Supabase API** - `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- [ ] **Gmail OAuth2** - Google account setup required
- [ ] **Google Calendar OAuth2** - Google account setup required

## ⏰ Backup Schedule

- **Manual:** Run `.\backup_n8n.ps1` anytime
- **Automated:** Daily at 2:00 AM (if set up)
- **Before Changes:** Always backup before major workflow modifications

## 🛡️ Best Practices

1. **Run backups before making changes**
2. **Keep multiple backup versions**
3. **Document your credential setup process**
4. **Test restoration periodically**
5. **Store backups in cloud storage (OneDrive, Google Drive, etc.)**

## 🔧 Troubleshooting

### Backup Fails
- Ensure n8n is running: `docker ps | findstr n8n`
- Check API key in backup script matches current n8n key
- Run as Administrator for automated setup

### Restore Fails
- Check n8n is accessible at `http://localhost:5678`
- Verify API key in import scripts
- Check Docker container has proper permissions

### Persistent Volumes Not Working
- Run `.\setup_n8n_persistent.ps1` again
- Check that `n8n-data` and `n8n-config` directories exist
- Verify Docker can access the mounted directories

## 📞 Support

If you encounter issues:
1. Check the backup logs in `backups/latest/BACKUP_INFO.txt`
2. Verify n8n container is running: `docker ps`
3. Test API access: `curl http://localhost:5678/api/v1/workflows`
4. Check this README for your specific scenario

---

**Remember:** With persistent volumes set up, you should never lose data again! 🎉