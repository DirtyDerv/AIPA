#!/usr/bin/env python3

import requests
import json
import time

N8N_URL = 'http://192.168.0.14:5678'
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

headers = {
    'X-N8N-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}

def fix_workflow_activation(workflow_id):
    """Fix workflow activation by deactivating and reactivating"""
    print(f"🔧 Fixing activation for workflow: {workflow_id}")
    
    try:
        # First check current status
        response = requests.get(f'{N8N_URL}/api/v1/workflows/{workflow_id}', headers=headers)
        if response.status_code == 200:
            workflow = response.json()
            print(f"Current status: Active = {workflow.get('active', False)}")
        
        # Deactivate
        print("📴 Deactivating workflow...")
        deactivate_response = requests.post(f'{N8N_URL}/api/v1/workflows/{workflow_id}/deactivate', headers=headers)
        if deactivate_response.status_code == 200:
            print("✅ Workflow deactivated")
        else:
            print(f"❌ Deactivation failed: {deactivate_response.status_code}")
            return False
            
        # Wait a moment
        time.sleep(2)
        
        # Reactivate
        print("🟢 Reactivating workflow...")
        activate_response = requests.post(f'{N8N_URL}/api/v1/workflows/{workflow_id}/activate', headers=headers)
        if activate_response.status_code == 200:
            print("✅ Workflow reactivated")
        else:
            print(f"❌ Reactivation failed: {activate_response.status_code}")
            return False
            
        # Wait for activation to take effect
        time.sleep(3)
        
        # Verify status
        response = requests.get(f'{N8N_URL}/api/v1/workflows/{workflow_id}', headers=headers)
        if response.status_code == 200:
            workflow = response.json()
            is_active = workflow.get('active', False)
            print(f"Final status: Active = {is_active}")
            return is_active
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_webhook():
    """Test the webhook after reactivation"""
    webhook_url = f"{N8N_URL}/webhook/aipa"
    
    test_payload = {
        "command": "/help",
        "user": "test_user", 
        "timestamp": "2024-12-29T12:00:00Z"
    }
    
    print(f"\n🔍 Testing webhook: {webhook_url}")
    
    try:
        response = requests.post(webhook_url, json=test_payload, timeout=15)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
            print(f"📄 Response: {response.text}")
            return True
        else:
            print(f"❌ Webhook test failed with status {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test error: {e}")
        return False

if __name__ == "__main__":
    workflow_id = "37bzjMV88aYgjcCK"
    
    # Fix activation
    if fix_workflow_activation(workflow_id):
        # Test webhook
        test_webhook()
    else:
        print("❌ Failed to properly activate workflow")