#!/usr/bin/env python3
"""
Complete AIPA Project Upload to GitHub
Uploads ALL files including credentials and sensitive data as requested by user
"""

import os
import json
import base64
from pathlib import Path

# File listing from PowerShell command
PROJECT_FILES = [
    "activation_guide.md",
    "ACTIVATION_STEPS.md", 
    "agents/crew_system.py",
    "agents/finish_day_agent.py",
    "ai-prompts/email-classifier.md",
    "ai-prompts/executive-assistant.md",
    "bot/discord_bot_bmf.py",
    "bot/discord_bot_bmf_clean.py", 
    "bot/discord_bot_setup.py",
    "bot/discord_bot_simple.py",
    "bot/README.md",
    "check_gmail_workflows.py",
    "CLEANUP_COMPLETE.md",
    "config/configure_n8n.bat",
    "config/configure_n8n.sh",
    "config/credential_ids.json",
    "config/CREDENTIALS.md",  # This is the sensitive one user wants uploaded
    "config/GEMINI.md",
    "config/README.md", 
    "config/requirements.txt",
    "create_fresh_gmail_workflow.py",
    "database/schema.sql",
    "database/schema-v2-enhanced.sql",
    "docs/WORKLOG_COMPLETE.md",
    "docs/BMF_WORKFLOW_USAGE_GUIDE.md",
    "docs/DISCORD_SETUP_GUIDE.md",
    "docs/README.md",
    "gemini_migration_report.json",
    "gmail_labels_creator.gs",
    "gmail_organizer_setup_report.json",
    "GMAIL_WORKFLOW_CREATED.md",
    "GMAIL_WORKFLOW_READY.md",
    "main_interface_migration_report.json",
    "mcp-servers/gmail_server.py",
    "mcp-servers/supabase_server.py",
    "migration_test_report.json",
    "n8n_test_report.md",
    "n8n-workflows/01-telegram-interface-BUILD-GUIDE.md",
    "n8n-workflows/01-telegram-main-interface.json",
    "n8n-workflows/02-email-processing-ai.json",
    "n8n-workflows/02-email-processing-BUILD-GUIDE.md",
    "n8n-workflows/03-dj-booking-automation.json",
    "n8n-workflows/04-woodys-order-processing.json",
    "n8n-workflows/05-bmf-work-logging.json",
    "n8n-workflows/06-calendar-management.json",
    "n8n-workflows/07-business-intelligence.json",
    "n8n-workflows/08-marketing-campaigns.json",
    "n8n-workflows/README.md",
    "populate_gmail_workflow.py",
    "README.md",
    "restart_n8n.sh",
    "restart_n8n_docker.sh",
    "restart_n8n_windows.ps1",
    "restore_gmail_workflow.py",
    "SESSION_SUMMARY_2025-11-02.md",
    "setup_correct_gmail_workflow.py",
    "setup_gmail_cleanup_complete.py",
    "supabase_schema_simple.sql",
    "supabase_setup.sql",
    "tools/bmf_immediate.py",
    "tools/finish-day.py",
    "tools/FINISH-DAY-SETUP.md",
    "tools/fix_gmail_workflow.py",
    "tools/github_upload.py",
    "tools/import_workflows.py",
    "tools/organize_project.py",
    "tools/quick_cleanup.py",
    "tools/README.md",
    "tools/requirements.txt",
    "tools/test_gmail_connection.py",
    "unarchive_gmail_workflow.py",
    "web/bmf_quick_commands.html",
    "web/bmf_web_logger.html", 
    "web/README.md",
    "workflow_errors_report.md",
    "workflows/bmf_workflow_live.json",
    "workflows/bmf_workflow_new.json",
    "workflows/README.md",
    "workflows/telegram_interface_live.json",
    ".gitignore"
]

def print_upload_status():
    """Print what files will be uploaded"""
    print("=" * 80)
    print("🚀 COMPLETE AIPA PROJECT UPLOAD TO GITHUB")
    print("=" * 80)
    
    print(f"\n📊 UPLOAD SUMMARY:")
    print(f"   Repository: DirtyDerv/AIPA")
    print(f"   Branch: development") 
    print(f"   Total files to upload: {len(PROJECT_FILES)}")
    print(f"   Including sensitive credentials: YES")
    
    print(f"\n📁 FILE CATEGORIES:")
    
    categories = {
        "Configuration & Credentials": [f for f in PROJECT_FILES if f.startswith("config/")],
        "Documentation": [f for f in PROJECT_FILES if f.startswith("docs/")],
        "Discord Bot": [f for f in PROJECT_FILES if f.startswith("bot/")],
        "Tools & Scripts": [f for f in PROJECT_FILES if f.startswith("tools/")],
        "Web Interfaces": [f for f in PROJECT_FILES if f.startswith("web/")],
        "Database Schema": [f for f in PROJECT_FILES if f.startswith("database/")],
        "n8n Workflows": [f for f in PROJECT_FILES if f.startswith("n8n-workflows/") or f.startswith("workflows/")],
        "MCP Servers": [f for f in PROJECT_FILES if f.startswith("mcp-servers/")],
        "AI Agents": [f for f in PROJECT_FILES if f.startswith("agents/")],
        "Root Files": [f for f in PROJECT_FILES if "/" not in f]
    }
    
    for category, files in categories.items():
        if files:
            print(f"   {category}: {len(files)} files")
            for file in files[:3]:  # Show first 3 files
                print(f"     - {file}")
            if len(files) > 3:
                print(f"     ... and {len(files) - 3} more")
    
    print(f"\n🔐 SENSITIVE FILES INCLUDED:")
    sensitive_files = [
        "config/CREDENTIALS.md",
        "bot/discord_bot_bmf.py", 
        "config/credential_ids.json"
    ]
    
    for file in sensitive_files:
        if file in PROJECT_FILES:
            print(f"   ✅ {file}")
    
    print(f"\n⚠️  IMPORTANT NOTES:")
    print(f"   • ALL credentials and API keys will be uploaded")
    print(f"   • Discord bot tokens, Supabase keys, webhooks included")
    print(f"   • Repository will contain sensitive data as requested")
    print(f"   • .gitignore will be overridden for this upload")
    
    print(f"\n📋 NEXT STEPS:")
    print(f"   1. User requested ALL files uploaded including credentials")
    print(f"   2. Use push_files tool to upload files in batches") 
    print(f"   3. Files are organized and ready for GitHub")
    print(f"   4. Development branch will contain complete project")
    
    print(f"\n🎯 UPLOAD STATUS:")
    print(f"   Ready to upload: {len(PROJECT_FILES)} files")
    print(f"   Estimated upload batches: {(len(PROJECT_FILES) + 9) // 10}")
    print(f"   All project structure preserved")

def create_file_batches():
    """Create batches of files for upload"""
    batch_size = 10
    batches = []
    
    for i in range(0, len(PROJECT_FILES), batch_size):
        batch = PROJECT_FILES[i:i + batch_size]
        batches.append(batch)
    
    return batches

if __name__ == "__main__":
    print_upload_status()
    
    batches = create_file_batches()
    print(f"\n📦 UPLOAD BATCHES:")
    for i, batch in enumerate(batches, 1):
        print(f"   Batch {i}: {len(batch)} files")
        for file in batch:
            print(f"     - {file}")
        print()
    
    print("✅ Upload planning complete!")
    print("💡 Use mcp_mcp_docker_push_files tool to upload each batch systematically.")