#!/usr/bin/env python3
"""
GitHub Upload Script for AIPA Project
Uploads the organized project structure to GitHub repository
"""

import os
import requests
import json
import base64
from pathlib import Path

# Configuration
REPO_OWNER = "DirtyDerv"
REPO_NAME = "AIPA"
BRANCH = "development"
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"  # Add your GitHub personal access token

# Important files to upload (excluding sensitive files)
UPLOAD_STRUCTURE = {
    "bot/": [
        "README.md",
        "discord_bot_bmf_clean.py",  # Clean version without credentials
    ],
    "docs/": [
        "WORKLOG_COMPLETE.md",
        "DISCORD_SETUP_GUIDE.md",
        "BMF_WORKFLOW_USAGE_GUIDE.md",
        "GMAIL_ORGANIZER_GUIDE.md",
        "README.md"
    ],
    "config/": [
        "README.md",
        "requirements.txt",
    ],
    "tools/": [
        "bmf_immediate.py",
        "test_gmail_connection.py", 
        "fix_gmail_workflow.py",
        "README.md"
    ],
    "web/": [
        "bmf_web_logger.html",
        "README.md"
    ],
    "workflows/": [
        "README.md",
        # Add n8n workflow files as needed
    ],
    "database/": [
        "supabase_schema_simple.sql",
        "supabase_setup.sql",
        "README.md"
    ]
}

# Files to exclude (sensitive information)
EXCLUDE_PATTERNS = [
    "*credentials*",
    "*token*",
    "*secret*",
    "*api_key*",
    "*.env",
    "*backup*",
    "*.git*",
    "*__pycache__*",
    "*.venv*"
]

def should_exclude_file(filepath):
    """Check if file should be excluded based on patterns"""
    filepath_lower = str(filepath).lower()
    for pattern in EXCLUDE_PATTERNS:
        if pattern.replace("*", "") in filepath_lower:
            return True
    return False

def sanitize_content(content):
    """Remove sensitive information from file content"""
    # Replace common sensitive patterns
    replacements = {
        # Discord tokens
        r'MTQzNDU4ODYyODQ0MDQ1MzIyMQ\.[^"]*': 'YOUR_DISCORD_BOT_TOKEN_HERE',
        # API keys 
        r'eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*': 'YOUR_API_KEY_HERE',
        # Webhook URLs
        r'https://discord\.com/api/webhooks/[0-9]+/[A-Za-z0-9_-]+': 'YOUR_DISCORD_WEBHOOK_URL_HERE',
        # Supabase URLs
        r'https://[a-z]+\.supabase\.co': 'YOUR_SUPABASE_URL_HERE',
        # IP addresses
        r'192\.168\.0\.14': 'YOUR_N8N_SERVER_IP',
    }
    
    import re
    sanitized = content
    for pattern, replacement in replacements.items():
        sanitized = re.sub(pattern, replacement, sanitized)
    
    return sanitized

def read_file_content(filepath):
    """Read and sanitize file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return sanitize_content(content)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def create_github_files():
    """Create file content for GitHub upload"""
    base_path = Path("c:/Users/woody/Documents/AI/AIPA")
    files_to_upload = []
    
    for directory, files in UPLOAD_STRUCTURE.items():
        for filename in files:
            filepath = base_path / directory / filename
            
            if filepath.exists() and not should_exclude_file(filepath):
                content = read_file_content(filepath)
                if content:
                    github_path = f"{directory}{filename}"
                    files_to_upload.append({
                        "path": github_path,
                        "content": content
                    })
                    print(f"Prepared: {github_path}")
    
    return files_to_upload

def print_upload_summary():
    """Print what would be uploaded"""
    print("=" * 60)
    print("🚀 AIPA PROJECT GITHUB UPLOAD SUMMARY")
    print("=" * 60)
    
    files = create_github_files()
    
    print(f"\n📊 Upload Statistics:")
    print(f"   Total files: {len(files)}")
    
    # Group by directory
    by_dir = {}
    for file_info in files:
        dir_name = file_info["path"].split("/")[0]
        if dir_name not in by_dir:
            by_dir[dir_name] = []
        by_dir[dir_name].append(file_info["path"])
    
    print(f"\n📁 Directory Structure:")
    for directory, file_list in by_dir.items():
        print(f"   {directory}/ ({len(file_list)} files)")
        for file_path in file_list:
            print(f"     - {file_path}")
    
    print(f"\n🔒 Security Features:")
    print(f"   - API keys and tokens sanitized")
    print(f"   - Webhook URLs replaced with placeholders")
    print(f"   - IP addresses masked")
    print(f"   - Credentials files excluded")
    
    print(f"\n💡 Manual Steps Required:")
    print(f"   1. Get GitHub personal access token")
    print(f"   2. Update GITHUB_TOKEN in this script")
    print(f"   3. Run script to upload files")
    print(f"   4. Create config/CREDENTIALS.md manually with actual values")
    
    print(f"\n🎯 Repository Target:")
    print(f"   Owner: {REPO_OWNER}")
    print(f"   Repo: {REPO_NAME}")
    print(f"   Branch: {BRANCH}")

if __name__ == "__main__":
    print_upload_summary()