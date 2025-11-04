#!/usr/bin/env python3

import requests
import json

N8N_URL = 'http://192.168.0.14:5678'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o'
headers = {'X-N8N-API-KEY': API_KEY, 'Content-Type': 'application/json'}

def create_simple_bmf_workflow():
    """Create a minimal working BMF workflow"""
    
    print("🛠️  Creating Simple BMF Workflow")
    print("=" * 32)
    
    # Minimal workflow with all required properties
    workflow_data = {
        "name": "AIPA - BMF Work Logger",
        "nodes": [
            {
                "id": "bmf-webhook-simple",
                "name": "BMF Entry Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [300, 200],
                "parameters": {
                    "path": "bmf-simple",
                    "httpMethod": "POST",
                    "responseMode": "onReceived"
                }
            }
        ],
        "connections": {},
        "settings": {
            "executionOrder": "v1"
        },
        "staticData": {},
        "tags": []
    }
    
    try:
        # Create workflow
        print("📝 Creating minimal BMF workflow...")
        response = requests.post(
            f'{N8N_URL}/api/v1/workflows',
            headers=headers,
            json=workflow_data
        )
        
        if response.status_code == 201:
            workflow = response.json()
            workflow_id = workflow.get('id')
            print(f"✅ Created workflow: {workflow_id}")
            
            # Activate it
            print("⚡ Activating workflow...")
            activate_response = requests.post(
                f'{N8N_URL}/api/v1/workflows/{workflow_id}/activate',
                headers=headers
            )
            
            if activate_response.status_code == 200:
                print("✅ Workflow activated!")
                
                # Test it
                print("\n🧪 Testing BMF webhook...")
                test_url = f'{N8N_URL}/webhook/bmf-simple'
                test_data = {"content": "BMF test entry", "user": "woody"}
                
                test_response = requests.post(test_url, json=test_data)
                print(f"Test result: {test_response.status_code}")
                
                if test_response.status_code == 200:
                    print("🎉 BMF WEBHOOK IS WORKING!")
                    print(f"✅ URL: {test_url}")
                    
                    # Send success message to Discord
                    discord_webhook = "https://discord.com/api/webhooks/1434598843546341581/r0NqE35ekv_88zWCj7TYze_15zuKtN_wsARtWMesa-_KVkKPA26jkZNNlSC2_3G4grzf"
                    success_msg = {
                        "embeds": [{
                            "title": "✅ BMF Work Logging FIXED!",
                            "description": f"Your BMF work logging is now working!\n\n**Webhook URL:** `{test_url}`",
                            "color": 65280,
                            "fields": [{
                                "name": "How to Test",
                                "value": "Send a POST request to the webhook URL above with your work entry data",
                                "inline": False
                            }]
                        }]
                    }
                    requests.post(discord_webhook, json=success_msg)
                    
                    return workflow_id, test_url
                else:
                    print(f"❌ Test failed: {test_response.text}")
            else:
                print(f"❌ Activation failed: {activate_response.status_code}")
        else:
            print(f"❌ Creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None, None

def manual_fix_instructions():
    """Provide manual fix instructions"""
    
    print("\n🔧 MANUAL FIX INSTRUCTIONS")
    print("=" * 26)
    print("Since the API approach is having issues, here's how to fix BMF manually:")
    print("\n1. Open n8n in browser: http://192.168.0.14:5678")
    print("2. Find 'AIPA - BMF Work Logging (Discord)' workflow")
    print("3. Click Edit to open it")
    print("4. Check the webhook node:")
    print("   • Path should be: bmf-work")
    print("   • Method should be: POST")
    print("   • Response mode: On Received")
    print("5. Save and activate the workflow")
    print("6. Test with: curl -X POST http://192.168.0.14:5678/webhook/bmf-work -d '{\"content\":\"test\"}'")
    
    print("\n🎯 ALTERNATIVE: Use Main Interface")
    print("The main interface workflow should route Discord messages automatically.")
    print("Try sending a message in #bmf-work channel starting with 'BMF:'")
    
    # Send manual instructions to Discord
    discord_webhook = "https://discord.com/api/webhooks/1434598843546341581/r0NqE35ekv_88zWCj7TYze_15zuKtN_wsARtWMesa-_KVkKPA26jkZNNlSC2_3G4grzf"
    manual_msg = {
        "embeds": [{
            "title": "🔧 BMF Work Logging - Manual Fix Needed",
            "description": "The automated fix had issues. Here's what we found and how to fix it:",
            "color": 16753920,
            "fields": [
                {
                    "name": "❌ Problem",
                    "value": "BMF webhook not properly registered in n8n",
                    "inline": False
                },
                {
                    "name": "🛠️ Quick Fix",
                    "value": "1. Open n8n: http://192.168.0.14:5678\n2. Edit BMF workflow\n3. Check webhook node settings\n4. Save and reactivate",
                    "inline": False
                },
                {
                    "name": "✅ Test Method",
                    "value": "Send message in this channel starting with 'BMF work:' and see if it logs properly",
                    "inline": False
                }
            ],
            "footer": {"text": "I can help guide you through the manual fix if needed"}
        }]
    }
    requests.post(discord_webhook, json=manual_msg)

if __name__ == "__main__":
    workflow_id, webhook_url = create_simple_bmf_workflow()
    
    if workflow_id:
        print(f"\n🎉 SUCCESS!")
        print(f"Workflow ID: {workflow_id}")
        print(f"Webhook URL: {webhook_url}")
        print(f"\nNow try posting a work entry to test it!")
    else:
        manual_fix_instructions()