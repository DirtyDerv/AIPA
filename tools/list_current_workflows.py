#!/usr/bin/env python3
"""
Direct n8n API Test - List Workflows
Tests direct API access to n8n server
"""

import requests
import json

# n8n Configuration from CREDENTIALS.md
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def test_connection():
    """Test n8n API connection"""
    print("🔍 Testing n8n API connection...")
    try:
        # Test basic connection
        response = requests.get(f"{N8N_URL}/api/v1/workflows", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            workflows = response.json()
            print(f"✅ Connected! Found {len(workflows.get('data', []))} workflows")
            return workflows
        else:
            print(f"❌ Failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def list_workflows(workflows_data):
    """List all workflows"""
    if not workflows_data or 'data' not in workflows_data:
        print("❌ No workflow data available")
        return
    
    workflows = workflows_data['data']
    print(f"\n📋 Current n8n Workflows ({len(workflows)}):")
    print("=" * 50)
    
    telegram_workflows = []
    other_workflows = []
    
    for workflow in workflows:
        name = workflow.get('name', 'Unnamed')
        active = "🟢 Active" if workflow.get('active', False) else "🔴 Inactive"
        id_str = workflow.get('id', 'No ID')
        
        # Check if it's a Telegram workflow
        if 'telegram' in name.lower() or 'aipa' in name.lower():
            telegram_workflows.append(workflow)
            print(f"📱 {name} ({id_str}) - {active} [TELEGRAM]")
        else:
            other_workflows.append(workflow)
            print(f"📊 {name} ({id_str}) - {active}")
    
    print(f"\n📊 Summary:")
    print(f"📱 Telegram workflows to migrate: {len(telegram_workflows)}")
    print(f"📊 Other workflows: {len(other_workflows)}")
    
    return telegram_workflows, other_workflows

def main():
    """Main function"""
    print("🚀 n8n Workflow Migration Assessment")
    print("=" * 40)
    print()
    
    # Test connection and get workflows
    workflows_data = test_connection()
    
    if workflows_data:
        list_workflows(workflows_data)
        print()
        print("📋 Next Steps:")
        print("1. Review Telegram workflows for migration")
        print("2. Update Telegram nodes to Discord webhooks")
        print("3. Test migrated workflows")
        print("4. Activate Discord-based workflows")
    else:
        print("❌ Cannot proceed without n8n connection")

if __name__ == "__main__":
    main()