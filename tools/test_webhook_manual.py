#!/usr/bin/env python3

import requests
import json

N8N_URL = 'http://192.168.0.14:5678'

def test_webhook():
    """Test the main interface webhook"""
    webhook_url = f"{N8N_URL}/webhook/aipa"
    
    test_payload = {
        "command": "/help",
        "user": "test_user", 
        "timestamp": "2024-12-29T12:00:00Z"
    }
    
    print(f"🔍 Testing webhook: {webhook_url}")
    print(f"📦 Payload: {json.dumps(test_payload, indent=2)}")
    
    try:
        response = requests.post(webhook_url, json=test_payload, timeout=15)
        print(f"📊 Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
            return True
        else:
            print(f"❌ Webhook test failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test error: {e}")
        return False

if __name__ == "__main__":
    test_webhook()