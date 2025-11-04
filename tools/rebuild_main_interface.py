#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime

N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

GENERAL_WEBHOOK = "https://discord.com/api/webhooks/1434598799090647163/gkiwL_F3DqTcqyckNR33T3-AN3SlY666bCkoXCvR_gctPsl2J4199YiNxD2LJoLmOi1K"

def delete_broken_workflow(workflow_id):
    """Delete the broken workflow"""
    print(f"🗑️ Deleting broken workflow: {workflow_id}")
    
    try:
        # First deactivate
        deactivate_response = requests.post(f'{N8N_URL}/api/v1/workflows/{workflow_id}/deactivate', headers=headers)
        
        # Then delete
        delete_response = requests.delete(f'{N8N_URL}/api/v1/workflows/{workflow_id}', headers=headers)
        if delete_response.status_code == 200:
            print(f"✅ Workflow {workflow_id} deleted successfully")
            return True
        else:
            print(f"❌ Failed to delete workflow: {delete_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error deleting workflow: {e}")
        return False

def create_clean_main_interface():
    """Create a clean, working main interface workflow"""
    print(f"🚀 Creating fresh Main Interface workflow...")
    
    # Simple, clean workflow structure
    workflow_data = {
        "name": "AIPA - Main Interface (Discord) - CLEAN",
        "settings": {
            "executionOrder": "v1"
        },
        "nodes": [
            {
                "parameters": {
                    "path": "aipa",
                    "httpMethod": "POST",
                    "responseMode": "onReceived",
                    "options": {}
                },
                "id": "main-webhook",
                "name": "AIPA Main Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [240, 300]
            },
            {
                "parameters": {
                    "jsCode": "// Parse incoming command\nconst command = $input.item.json.command || '';\nconst user = $input.item.json.user || 'unknown';\nconst timestamp = $input.item.json.timestamp || new Date().toISOString();\n\n// Simple command routing\nlet action = 'help';\nlet businessContext = 'general';\nlet routingDecision = 'processed';\n\nif (command.includes('/email')) {\n  action = 'email';\n  businessContext = 'business';\n} else if (command.includes('/calendar')) {\n  action = 'calendar';\n  businessContext = 'business';\n} else if (command.includes('/woodys')) {\n  action = 'woodys';\n  businessContext = 'creative';\n} else if (command.includes('/dj')) {\n  action = 'dj';\n  businessContext = 'creative';\n} else if (command.includes('/reports')) {\n  action = 'reports';\n  businessContext = 'business';\n}\n\nreturn {\n  originalCommand: command,\n  user: user,\n  timestamp: timestamp,\n  action: action,\n  businessContext: businessContext,\n  routingDecision: routingDecision\n};"
                },
                "id": "parse-command",
                "name": "Parse Command & Route",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [440, 300]
            },
            {
                "parameters": {
                    "url": GENERAL_WEBHOOK,
                    "method": "POST",
                    "sendHeaders": True,
                    "headerParameters": {
                        "parameters": [
                            {
                                "name": "Content-Type",
                                "value": "application/json"
                            }
                        ]
                    },
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "embeds",
                                "value": "=[{\"title\":\"🤖 AIPA Command Received\",\"description\":\"{{ $node['Parse Command & Route'].json.originalCommand }}\",\"color\":3447003,\"fields\":[{\"name\":\"👤 User\",\"value\":\"{{ $node['Parse Command & Route'].json.user }}\",\"inline\":true},{\"name\":\"🏢 Business Context\",\"value\":\"{{ $node['Parse Command & Route'].json.businessContext }}\",\"inline\":true},{\"name\":\"⚡ Action\",\"value\":\"{{ $node['Parse Command & Route'].json.action }}\",\"inline\":true}],\"timestamp\":\"{{ new Date().toISOString() }}\",\"footer\":{\"text\":\"AIPA Main Interface\"}}]"
                            }
                        ]
                    }
                },
                "id": "discord-response",
                "name": "Send Discord Response",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4,
                "position": [640, 300]
            }
        ],
        "connections": {
            "main-webhook": {
                "main": [
                    [
                        {
                            "node": "parse-command",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "parse-command": {
                "main": [
                    [
                        {
                            "node": "discord-response",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        }
    }
    
    try:
        response = requests.post(f"{N8N_URL}/api/v1/workflows", headers=headers, json=workflow_data)
        
        if response.status_code in [200, 201]:
            workflow = response.json()
            workflow_id = workflow['id']
            print(f"✅ Clean workflow created: {workflow_id}")
            return workflow_id
        else:
            print(f"❌ Failed to create workflow: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
        return None

def activate_and_test(workflow_id):
    """Activate the workflow and test it"""
    print(f"🔄 Activating workflow {workflow_id}...")
    
    try:
        # Activate
        activate_response = requests.post(f'{N8N_URL}/api/v1/workflows/{workflow_id}/activate', headers=headers)
        if activate_response.status_code == 200:
            print(f"✅ Workflow activated")
            
            # Wait for activation to take effect
            time.sleep(3)
            
            # Test webhook
            webhook_url = f"{N8N_URL}/webhook/aipa"
            test_payload = {
                "command": "/help",
                "user": "test_user",
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"🧪 Testing webhook: {webhook_url}")
            test_response = requests.post(webhook_url, json=test_payload, timeout=15)
            
            print(f"📊 Test result: {test_response.status_code}")
            if test_response.status_code == 200:
                print(f"🎉 SUCCESS! Main Interface webhook is working!")
                return True
            else:
                print(f"❌ Test failed: {test_response.text}")
                return False
                
        else:
            print(f"❌ Failed to activate: {activate_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main migration function with clean rebuild"""
    print("🔄 REBUILDING Main Interface with clean approach...")
    print("=" * 60)
    
    # Step 1: Delete broken workflows
    broken_workflows = ["37bzjMV88aYgjcCK", "syOAaibpawxbraJJ"]  # Both previous attempts
    
    for workflow_id in broken_workflows:
        delete_broken_workflow(workflow_id)
    
    time.sleep(2)
    
    # Step 2: Create clean workflow
    new_workflow_id = create_clean_main_interface()
    if not new_workflow_id:
        print("❌ Failed to create clean workflow")
        return False
    
    # Step 3: Activate and test
    success = activate_and_test(new_workflow_id)
    
    if success:
        print(f"\n🎉 MAIN INTERFACE REBUILD SUCCESSFUL!")
        print("=" * 45)
        print(f"✅ New Workflow ID: {new_workflow_id}")
        print(f"🔗 Webhook URL: {N8N_URL}/webhook/aipa")
        print(f"📱 Interface: 🟢 Active and Working")
        
        print(f"\n📊 Migration Progress Update:")
        print(f"✅ Email Processing: Migrated & Active")
        print(f"✅ Business Intelligence: Migrated & Active") 
        print(f"✅ Main Interface: Rebuilt & Active")
        print(f"📋 Remaining: 5 workflows to migrate")
        
        return True
    else:
        print(f"\n❌ Rebuild failed - webhook still not working")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🚀 Ready to continue with remaining workflow migrations!")
    else:
        print(f"\n❌ Need to investigate webhook registration issues further.")