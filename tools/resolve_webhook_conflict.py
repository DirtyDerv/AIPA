#!/usr/bin/env python3

import requests
import json

N8N_URL = 'http://192.168.0.14:5678'
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"

headers = {
    'X-N8N-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}

def check_telegram_workflow():
    """Check the original Telegram main interface workflow"""
    original_id = "DRuQZOp9tM79Sf6D"
    
    try:
        response = requests.get(f'{N8N_URL}/api/v1/workflows/{original_id}', headers=headers)
        if response.status_code == 200:
            workflow = response.json()
            print(f"✅ Original Telegram workflow found:")
            print(f"  Name: {workflow.get('name', 'Unknown')}")
            print(f"  Active: {workflow.get('active', False)}")
            
            # Check for webhook nodes
            nodes = workflow.get('nodes', [])
            webhook_nodes = [node for node in nodes if node.get('type') == 'n8n-nodes-base.webhook']
            
            if webhook_nodes:
                print(f"  Webhook nodes: {len(webhook_nodes)}")
                for i, node in enumerate(webhook_nodes):
                    params = node.get('parameters', {})
                    path = params.get('path', '')
                    method = params.get('httpMethod', 'GET')
                    print(f"    Webhook {i+1}: {method} /{path}")
                    
                    if path == 'aipa':
                        print(f"      ⚠️  CONFLICT: This workflow also uses 'aipa' path!")
                        
                        if workflow.get('active', False):
                            print(f"      🔴 CRITICAL: Both workflows are active with same webhook path!")
                            return True  # Conflict detected
            else:
                print(f"  No webhook nodes found")
                
        elif response.status_code == 404:
            print(f"✅ Original Telegram workflow not found (probably deleted)")
        else:
            print(f"❌ Error checking original workflow: {response.status_code}")
            
        return False  # No conflict
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def deactivate_telegram_if_needed():
    """Deactivate the Telegram workflow if it's causing conflicts"""
    original_id = "DRuQZOp9tM79Sf6D"
    
    try:
        # Check if it's active
        response = requests.get(f'{N8N_URL}/api/v1/workflows/{original_id}', headers=headers)
        if response.status_code == 200:
            workflow = response.json()
            if workflow.get('active', False):
                print(f"\n🔧 Deactivating conflicting Telegram workflow...")
                deactivate_response = requests.post(f'{N8N_URL}/api/v1/workflows/{original_id}/deactivate', headers=headers)
                if deactivate_response.status_code == 200:
                    print(f"✅ Telegram workflow deactivated")
                    return True
                else:
                    print(f"❌ Failed to deactivate: {deactivate_response.status_code}")
            else:
                print(f"✅ Telegram workflow already inactive")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        
    return False

if __name__ == "__main__":
    print("🔍 Checking for Telegram workflow conflicts...")
    
    has_conflict = check_telegram_workflow()
    
    if has_conflict:
        print(f"\n🚨 CONFLICT DETECTED! Attempting to resolve...")
        if deactivate_telegram_if_needed():
            print(f"\n✅ Conflict resolved. Testing webhook now...")
            
            # Test the webhook after resolving conflict
            import time
            time.sleep(2)
            
            webhook_url = f"{N8N_URL}/webhook/aipa"
            test_payload = {"command": "/help", "user": "test_user", "timestamp": "2024-12-29T12:00:00Z"}
            
            try:
                response = requests.post(webhook_url, json=test_payload, timeout=15)
                print(f"📊 Webhook test result: {response.status_code}")
                if response.status_code == 200:
                    print(f"🎉 SUCCESS! Webhook is now working!")
                else:
                    print(f"❌ Still not working: {response.text}")
            except Exception as e:
                print(f"❌ Test error: {e}")
    else:
        print(f"\n✅ No conflicts detected with Telegram workflow.")
        
        # Still test the webhook to see if the issue is elsewhere
        webhook_url = f"{N8N_URL}/webhook/aipa"
        test_payload = {"command": "/help", "user": "test_user", "timestamp": "2024-12-29T12:00:00Z"}
        
        try:
            response = requests.post(webhook_url, json=test_payload, timeout=15)
            print(f"📊 Webhook test result: {response.status_code}")
            if response.status_code == 200:
                print(f"🎉 Webhook is working!")
            else:
                print(f"❌ Webhook issue persists: {response.text}")
        except Exception as e:
            print(f"❌ Test error: {e}")