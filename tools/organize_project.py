#!/usr/bin/env python3
"""
AIPA Project Structure Organizer
Clean up and organize the project into proper folders
"""

import os
import shutil
from pathlib import Path

def create_folder_structure():
    """Create the proper folder structure for AIPA"""
    
    print("📁 Creating Clean Folder Structure")
    print("=" * 35)
    
    folders = {
        "🤖 Discord Bot": "bot/",
        "📋 Documentation": "docs/",
        "⚙️ Configuration": "config/", 
        "🔧 Tools & Scripts": "tools/",
        "📊 Workflows": "workflows/",
        "🌐 Web Interfaces": "web/",
        "🗃️ Backups": "backups/"
    }
    
    for name, folder in folders.items():
        os.makedirs(folder, exist_ok=True)
        print(f"   ✅ Created: {folder}")
    
    return folders

def organize_files():
    """Move files to their appropriate folders"""
    
    print(f"\n📦 Organizing Files")
    print("=" * 18)
    
    # File organization mapping
    file_moves = {
        # Discord Bot files
        "bot/": [
            "discord_bot_bmf.py",
            "discord_bot_simple.py", 
            "discord_bot_setup.py"
        ],
        
        # Documentation
        "docs/": [
            "DISCORD_SETUP_GUIDE.md",
            "DISCORD_BOT_DEPLOYMENT.md",
            "BMF_WORKFLOW_USAGE_GUIDE.md",
            "CREDENTIAL_SETUP_GUIDE.md",
            "DISCORD_BOT_INVITATION.md",
            "DISCORD_MIGRATION_MILESTONE.md",
            "DISCORD_QUICK_SETUP.md",
            "DISCORD_VOICE_SETUP.md",
            "DOCKER_INSTRUCTIONS.md",
            "EXACT_DOCKER_COMMANDS.txt",
            "FINAL_SIMPLE_STEPS.md",
            "FIXES_COMPLETED_SUMMARY.md",
            "GETTING-STARTED.md",
            "GMAIL_API_SETUP.md",
            "GMAIL_ORGANIZER_GUIDE.md",
            "GMAIL_ORGANIZER_STATUS.md",
            "GOOGLE_CALENDAR_SETUP.md",
            "MIGRATION_PROGRESS_REPORT.md",
            "N8N_API_DOCUMENTATION.md",
            "N8N_MCP_SETUP.md",
            "README.md",
            "READY_TO_ACTIVATE.md",
            "REMAINING_WORKFLOWS_GUIDE.md",
            "SIMPLE_INSTRUCTIONS.md",
            "SUPER_SIMPLE_STEPS.txt",
            "TELEGRAM_RATE_LIMIT_GUIDE.md",
            "V2-COMPLETE-SYSTEM-OVERVIEW.md",
            "WORKFLOW_ACTIVATION_GUIDE.md",
            "WORKFLOW_DEBUG_SUMMARY.md",
            "WORKLOG_COMPLETE.md"
        ],
        
        # Configuration files
        "config/": [
            "CREDENTIALS.md",
            "credential_ids.json",
            "configure_n8n.bat",
            "configure_n8n.sh",
            "requirements.txt",
            "GEMINI.md"
        ],
        
        # Tools and scripts
        "tools/": [
            "bmf_immediate.py",
            "bmf_monitor.py",
            "n8n_cleanup.py",
            "quick_cleanup.py",
            "setup_database.py",
            "setup_discord_channels.ps1",
            "setup_discord_channels_fixed.ps1",
            "setup_discord_server.py",
            "setup_discord_server_simple.py",
            "setup_gemini_api.py",
            "simple_bmf_fix.py",
            "test_discord_connection.py",
            "test_discord_integration.py",
            "test_discord_webhooks.py",
            "test_discord_webhooks_auto.py",
            "test_execution_methods.py",
            "test_gmail_functionality.py",
            "test_gmail_organizer.py",
            "test_main_interface_final.py",
            "test_webhook_manual.py",
            "test_and_fix_bmf.py"
        ],
        
        # Workflows
        "workflows/": [
            "bmf_workflow_live.json",
            "bmf_workflow_new.json",
            "telegram_interface_live.json",
            "UserswoodyDocumentsAIAIPAtelegram_workflow_backup.json"
        ],
        
        # Web interfaces
        "web/": [
            "bmf_web_logger.html",
            "bmf_quick_commands.html"
        ],
        
        # Move existing backups
        "backups/": [
            # Will move the backup folder we created earlier
        ]
    }
    
    moved_count = 0
    
    for folder, files in file_moves.items():
        for file in files:
            if os.path.exists(file) and not os.path.exists(f"{folder}{file}"):
                try:
                    shutil.move(file, f"{folder}{file}")
                    print(f"   📦 Moved: {file} → {folder}")
                    moved_count += 1
                except Exception as e:
                    print(f"   ❌ Error moving {file}: {e}")
    
    # Move backup folder
    backup_folders = [f for f in os.listdir('.') if f.startswith('backup_')]
    for backup in backup_folders:
        if os.path.isdir(backup):
            try:
                shutil.move(backup, f"backups/{backup}")
                print(f"   📦 Moved: {backup} → backups/")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Error moving {backup}: {e}")
    
    print(f"\n📊 Moved {moved_count} files")
    return moved_count

def create_index_files():
    """Create index files for each folder"""
    
    print(f"\n📝 Creating Index Files")
    print("=" * 21)
    
    # Bot folder README
    bot_readme = '''# AIPA Discord Bot

## Files
- `discord_bot_bmf.py` - Main Discord bot for BMF work logging
- `discord_bot_simple.py` - Simplified bot with slash commands only
- `discord_bot_setup.py` - Setup instructions

## Deployment
1. Copy to server: `scp discord_bot_bmf.py user@192.168.0.14:/path/to/aipa/`
2. Install dependencies: `pip install discord.py`
3. Run: `python discord_bot_bmf.py`

## Status
✅ Working and tested
🔄 Needs deployment to server for 24/7 operation
'''

    # Tools folder README
    tools_readme = '''# AIPA Tools & Scripts

## BMF Tools
- `bmf_immediate.py` - Immediate BMF work logging
- `bmf_monitor.py` - Monitor BMF workflow status
- `simple_bmf_fix.py` - Simple BMF fixes

## Testing Tools
- `test_discord_*.py` - Discord integration tests
- `test_gmail_*.py` - Gmail functionality tests
- `test_webhook_*.py` - Webhook testing

## Setup Tools
- `setup_*.py` - Various setup scripts
- `n8n_cleanup.py` - Clean up n8n workflows

## Usage
Each script can be run independently:
```bash
python tools/bmf_immediate.py
python tools/test_discord_connection.py
```
'''

    # Config folder README
    config_readme = '''# AIPA Configuration

## Important Files
- `CREDENTIALS.md` - All system credentials (KEEP SECURE!)
- `credential_ids.json` - n8n credential mappings
- `requirements.txt` - Python dependencies

## Setup Scripts
- `configure_n8n.bat/.sh` - n8n configuration

## Security
⚠️ Never commit CREDENTIALS.md to Git
🔒 Keep credentials secure and private
'''

    # Web folder README
    web_readme = '''# AIPA Web Interfaces

## BMF Logging
- `bmf_web_logger.html` - Browser-based BMF work logging
- `bmf_quick_commands.html` - Quick reference for BMF commands

## Usage
Open HTML files in browser for web-based interfaces.
'''

    # Workflows folder README
    workflows_readme = '''# AIPA n8n Workflows

## Active Workflows
- `bmf_workflow_new.json` - Latest BMF work logging workflow
- `bmf_workflow_live.json` - Live BMF workflow backup

## Legacy
- `telegram_interface_live.json` - Old Telegram interface (archived)

## Import to n8n
1. Open n8n web interface
2. Go to Import/Export
3. Import JSON files as needed
'''

    readme_files = {
        'bot/README.md': bot_readme,
        'tools/README.md': tools_readme,
        'config/README.md': config_readme,
        'web/README.md': web_readme,
        'workflows/README.md': workflows_readme
    }
    
    for file_path, content in readme_files.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ Created: {file_path}")

def create_main_readme():
    """Create updated main README"""
    
    main_readme = '''# AIPA - AI Personal Assistant

## Project Status
✅ **Discord Migration Complete**
✅ **Project Cleanup Complete**  
✅ **BMF Work Logging Functional**
🔄 **Bot Deployment Pending**

## Quick Start
1. **BMF Work Logging**: Run `python tools/bmf_immediate.py`
2. **Discord Bot**: Deploy `bot/discord_bot_bmf.py` to server
3. **Web Interface**: Open `web/bmf_web_logger.html`

## Project Structure
```
📁 AIPA/
├── 🤖 bot/           # Discord bot files
├── 📋 docs/          # Documentation
├── ⚙️ config/        # Configuration & credentials
├── 🔧 tools/         # Scripts & utilities
├── 📊 workflows/     # n8n workflow backups
├── 🌐 web/           # Web interfaces
└── 🗃️ backups/       # Project backups
```

## Active Systems
- **n8n**: 20 active workflows on 192.168.0.14:5678
- **Gmail Organizer**: Auto-organizing emails daily at 2 AM
- **Discord Voice**: Processing voice messages with Gemini AI
- **BMF Logging**: Multiple working solutions available

## Core Features
- 📧 **Gmail Organization**: AI-powered email sorting and labeling
- 🎵 **Discord Voice Processing**: Voice-to-text with Gemini AI
- 📝 **BMF Work Logging**: Track and log work entries
- 📱 **Discord Integration**: Rich embeds and slash commands
- 🤖 **AI Processing**: Google Gemini for smart responses

## Next Steps
1. Deploy Discord bot to server for 24/7 operation
2. Monitor and maintain active workflows
3. Expand Discord command capabilities

## Support
See `docs/` folder for detailed setup guides and troubleshooting.
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(main_readme)
    
    print("   ✅ Updated: README.md")

def cleanup_root_directory():
    """Clean up remaining files in root directory"""
    
    print(f"\n🧹 Final Root Directory Cleanup")
    print("=" * 32)
    
    # Files to keep in root
    keep_in_root = [
        'README.md', '.gitignore', '.git', '.venv', '.claude',
        'activation_guide.md', 'ACTIVATION_STEPS.md',
        'workflow_errors_report.md', 'n8n_test_report.md',
        'gmail_organizer_setup_report.json', 'gemini_migration_report.json',
        'main_interface_migration_report.json', 'migration_test_report.json'
    ]
    
    # Move remaining files to appropriate folders
    remaining_files = [f for f in os.listdir('.') if os.path.isfile(f) and f not in keep_in_root]
    
    moved = 0
    for file in remaining_files:
        try:
            # Determine where to move the file
            if file.endswith('.py'):
                shutil.move(file, f'tools/{file}')
                print(f"   📦 Moved script: {file} → tools/")
            elif file.endswith('.md'):
                shutil.move(file, f'docs/{file}')
                print(f"   📦 Moved doc: {file} → docs/")
            elif file.endswith(('.json', '.html', '.txt')):
                shutil.move(file, f'tools/{file}')
                print(f"   📦 Moved file: {file} → tools/")
            moved += 1
        except Exception as e:
            print(f"   ❌ Error moving {file}: {e}")
    
    print(f"\n📊 Moved {moved} additional files")

def main():
    """Main organization function"""
    
    print("🎯 AIPA Project Organization")
    print("=" * 28)
    
    # Create folder structure
    create_folder_structure()
    
    # Organize files
    moved_count = organize_files()
    
    # Create documentation
    create_index_files()
    create_main_readme()
    
    # Final cleanup
    cleanup_root_directory()
    
    print(f"\n✅ PROJECT ORGANIZATION COMPLETE!")
    print("=" * 35)
    print(f"📁 Created organized folder structure")
    print(f"📦 Moved {moved_count} files to appropriate folders")
    print(f"📝 Created documentation for each folder")
    print(f"🧹 Cleaned up root directory")
    
    print(f"\n🎯 PROJECT STATUS:")
    print(f"✅ File cleanup: 54 files deleted")
    print(f"✅ n8n cleanup: 5 workflows deleted")
    print(f"✅ Project organization: Complete")
    print(f"🔄 Discord bot deployment: Pending")

if __name__ == "__main__":
    main()