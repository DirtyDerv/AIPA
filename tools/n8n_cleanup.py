#!/usr/bin/env python3
"""
n8n Workflow Cleanup Script
List all workflows and identify which ones to keep/delete
"""

import requests
import json
from datetime import datetime

# n8n configuration from CREDENTIALS.md
N8N_URL = "http://192.168.0.14:5678"
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

def list_all_workflows():
    """List all workflows in n8n"""
    
    print("📋 Listing All n8n Workflows")
    print("=" * 30)
    
    try:
        response = requests.get(f"{N8N_URL}/api/v1/workflows", headers=headers)
        
        if response.status_code == 200:
            workflows = response.json()
            
            print(f"Found {len(workflows['data'])} workflows:")
            
            # Categorize workflows
            keep_workflows = []
            delete_workflows = []
            
            for workflow in workflows['data']:
                wf_id = workflow['id']
                wf_name = workflow['name']
                wf_active = workflow['active']
                wf_updated = workflow['updatedAt']
                
                print(f"\n🔍 {wf_name}")
                print(f"   ID: {wf_id}")
                print(f"   Active: {'✅' if wf_active else '❌'}")
                print(f"   Updated: {wf_updated}")
                
                # Determine if we should keep this workflow
                if should_keep_workflow(wf_name, wf_active):
                    keep_workflows.append((wf_id, wf_name, wf_active))
                    print(f"   Status: 🟢 KEEP")
                else:
                    delete_workflows.append((wf_id, wf_name, wf_active))
                    print(f"   Status: 🔴 DELETE")
            
            return keep_workflows, delete_workflows
            
        else:
            print(f"❌ Error listing workflows: {response.status_code}")
            print(f"Response: {response.text}")
            return [], []
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return [], []

def should_keep_workflow(name, active):
    """Determine if a workflow should be kept"""
    
    # Always keep these workflows
    keep_patterns = [
        "gmail",  # Gmail organizer
        "discord",  # Discord integrations
        "voice",  # Voice processing
        "bmf",  # BMF work logging
        "gemini",  # AI processing
        "calendar",  # Calendar integration
        "email"  # Email processing
    ]
    
    # Delete these workflows
    delete_patterns = [
        "telegram",  # Old Telegram workflows
        "test",  # Test workflows
        "backup",  # Backup workflows
        "old",  # Old workflows
        "temp",  # Temporary workflows
        "migration",  # Migration workflows
        "debug"  # Debug workflows
    ]
    
    name_lower = name.lower()
    
    # Check if it should be deleted
    for pattern in delete_patterns:
        if pattern in name_lower:
            return False
    
    # Check if it should be kept
    for pattern in keep_patterns:
        if pattern in name_lower:
            return True
    
    # If active, lean towards keeping
    if active:
        return True
    
    # Default: delete inactive unknown workflows
    return False

def delete_workflow(workflow_id, workflow_name):
    """Delete a specific workflow"""
    
    try:
        response = requests.delete(f"{N8N_URL}/api/v1/workflows/{workflow_id}", headers=headers)
        
        if response.status_code == 200:
            print(f"   ✅ Deleted: {workflow_name}")
            return True
        else:
            print(f"   ❌ Error deleting {workflow_name}: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error deleting {workflow_name}: {e}")
        return False

def cleanup_workflows():
    """Main cleanup function"""
    
    print("🧹 n8n Workflow Cleanup")
    print("=" * 24)
    
    # List all workflows
    keep_workflows, delete_workflows = list_all_workflows()
    
    if not keep_workflows and not delete_workflows:
        print("❌ Could not connect to n8n or no workflows found")
        return
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"Workflows to keep: {len(keep_workflows)}")
    print(f"Workflows to delete: {len(delete_workflows)}")
    
    if keep_workflows:
        print(f"\n🟢 WORKFLOWS TO KEEP:")
        for wf_id, wf_name, wf_active in keep_workflows:
            status = "Active" if wf_active else "Inactive"
            print(f"   ✅ {wf_name} ({status})")
    
    if delete_workflows:
        print(f"\n🔴 WORKFLOWS TO DELETE:")
        for wf_id, wf_name, wf_active in delete_workflows:
            status = "Active" if wf_active else "Inactive"
            print(f"   🗑️ {wf_name} ({status})")
        
        # Ask for confirmation
        print(f"\n⚠️ WARNING: This will permanently delete {len(delete_workflows)} workflows!")
        choice = input("Proceed with deletion? (y/N): ").strip().lower()
        
        if choice == 'y':
            print(f"\n🗑️ Deleting workflows...")
            deleted_count = 0
            
            for wf_id, wf_name, wf_active in delete_workflows:
                if delete_workflow(wf_id, wf_name):
                    deleted_count += 1
            
            print(f"\n✅ Cleanup complete!")
            print(f"   🗑️ Deleted: {deleted_count} workflows")
            print(f"   ✅ Kept: {len(keep_workflows)} workflows")
        else:
            print("❌ Cleanup cancelled")

if __name__ == "__main__":
    cleanup_workflows()