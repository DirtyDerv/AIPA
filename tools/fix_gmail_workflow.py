#!/usr/bin/env python3
"""
Gmail Workflow Fix Script
Diagnoses and fixes Gmail organization workflow issues
"""

import requests
import json
import webbrowser
from datetime import datetime

# n8n configuration
N8N_URL = "http://192.168.0.14:5678"
WORKFLOW_ID = "wnvzXLgk0W75yC4j"

def open_workflow_in_browser():
    """Open the Gmail workflow in n8n editor"""
    workflow_url = f"{N8N_URL}/workflow/{WORKFLOW_ID}"
    print(f"🌐 Opening Gmail workflow in browser...")
    print(f"   URL: {workflow_url}")
    
    try:
        webbrowser.open(workflow_url)
        print("✅ Browser opened! Please check the workflow.")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print(f"   Please manually go to: {workflow_url}")

def print_fix_instructions():
    """Print step-by-step fix instructions"""
    print("\n" + "=" * 60)
    print("🔧 GMAIL WORKFLOW FIX INSTRUCTIONS")
    print("=" * 60)
    
    print("\n1. 📧 GMAIL CREDENTIALS SETUP:")
    print("   - Go to: http://192.168.0.14:5678/credentials")
    print("   - Click 'Add Credential'")
    print("   - Select 'Gmail OAuth2 API'")
    print("   - Name it: 'Gmail - Woody'")
    print("   - Follow OAuth setup process")
    
    print("\n2. 🔗 LINK CREDENTIALS TO WORKFLOW:")
    print(f"   - Go to: {N8N_URL}/workflow/{WORKFLOW_ID}")
    print("   - Click on each Gmail node (5 nodes total):")
    print("     * Get Old Emails (1+ Years)")
    print("     * Get Spam Emails")
    print("     * Create Protected Label")
    print("     * Create Receipts Label") 
    print("     * Create Credentials Label")
    print("   - For each node, select 'Gmail - Woody' credential")
    print("   - Save the workflow")
    
    print("\n3. 🧪 TEST THE WORKFLOW:")
    print("   - Click 'Execute Workflow' button")
    print("   - Check if it runs without errors")
    print("   - Verify it creates labels in Gmail")
    
    print("\n4. ⏰ VERIFY SCHEDULE:")
    print("   - Check the Cron trigger node")
    print("   - Should be set to: '0 2 * * *' (daily at 2 AM)")
    print("   - Make sure workflow is 'Active'")
    
    print("\n💡 QUICK CHECK:")
    print("   The workflow had 1 successful execution but 0 credentials.")
    print("   This means it ran but couldn't connect to Gmail.")
    print("   After adding credentials, it should work properly.")

def check_current_status():
    """Show current workflow status"""
    print("\n📊 CURRENT STATUS:")
    print(f"   Workflow ID: {WORKFLOW_ID}")
    print(f"   Name: AIPA - Advanced Gmail Organization & Cleanup")
    print(f"   Status: ✅ Active")
    print(f"   Schedule: Daily at 2:00 AM")
    print(f"   Last Execution: 2025-11-02T20:27:45.730Z (Success)")
    print(f"   Issue: 🔑 No Gmail credentials configured")
    print(f"   Gmail Nodes: 5 nodes need credentials")

def main():
    print("=" * 60)
    print("🛠️  GMAIL ORGANIZATION WORKFLOW FIXER")
    print("=" * 60)
    
    check_current_status()
    print_fix_instructions()
    
    print("\n" + "=" * 60)
    print("🚀 QUICK ACTION")
    print("=" * 60)
    
    response = input("Open workflow in browser now? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        open_workflow_in_browser()
    
    print("\n✅ Once you've added the Gmail credentials to all 5 nodes,")
    print("   the workflow will automatically organize your emails daily!")

if __name__ == "__main__":
    main()