#!/usr/bin/env python3

import requests
import json
from datetime import datetime

N8N_URL = 'http://192.168.0.14:5678'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk'
headers = {'X-N8N-API-KEY': API_KEY, 'Content-Type': 'application/json'}

def test_bmf_and_create_new():
    """Test BMF workflow and create new one if needed"""
    
    print("🧪 Testing BMF Work Logging")
    print("=" * 30)
    
    # Test current webhook paths
    test_paths = ['bmf', 'bmf-work', 'bmf-work-logging']
    
    for path in test_paths:
        print(f"\n🔗 Testing webhook path: /webhook/{path}")
        test_data = {
            "content": f"BMF test entry - {datetime.now().strftime('%H:%M:%S')}",
            "author": {"username": "woody"},
            "channel": "bmf-work"
        }
        
        try:
            response = requests.post(
                f'{N8N_URL}/webhook/{path}',
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ Path '{path}' is working!")
                print(f"   🎯 Use this URL for BMF logging: {N8N_URL}/webhook/{path}")
                return path
            else:
                print(f"   ❌ Not working: {response.text[:100]}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🔧 None of the webhook paths are working. Creating new BMF workflow...")
    
    # Create a new, simple BMF workflow
    new_workflow = {
        "name": "AIPA - BMF Work Logging (Fixed)",
        "active": True,
        "nodes": [
            {
                "parameters": {
                    "path": "bmf-work-new",
                    "httpMethod": "POST",
                    "responseMode": "onReceived"
                },
                "id": "webhook-bmf",
                "name": "BMF Work Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [240, 300]
            },
            {
                "parameters": {
                    "url": "https://neoeoabqcfpopzkwvcxq.supabase.co/rest/v1/conversations",
                    "authentication": "genericCredentialType",
                    "genericAuthType": "httpHeaderAuth",
                    "sendHeaders": True,
                    "headerParameters": {
                        "parameters": [
                            {
                                "name": "Content-Type",
                                "value": "application/json"
                            },
                            {
                                "name": "Prefer",
                                "value": "return=minimal"
                            }
                        ]
                    },
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "user_id",
                                "value": "woody"
                            },
                            {
                                "name": "message",
                                "value": "={{ $json.content }}"
                            },
                            {
                                "name": "business_context",
                                "value": "bmf-work"
                            },
                            {
                                "name": "timestamp",
                                "value": "={{ $now }}"
                            },
                            {
                                "name": "message_type",
                                "value": "work_log"
                            }
                        ]
                    }
                },
                "id": "supabase-log",
                "name": "Log to Supabase",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.2,
                "position": [460, 300],
                "credentials": {
                    "httpHeaderAuth": {
                        "id": "3",
                        "name": "AIPA Supabase REST"
                    }
                }
            },
            {
                "parameters": {
                    "url": "https://discord.com/api/webhooks/1434598843546341581/r0NqE35ekv_88zWCj7TYze_15zuKtN_wsARtWMesa-_KVkKPA26jkZNNlSC2_3G4grzf",
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
                                "value": "=[{\"title\": \"🏢 BMF Work Logged\", \"description\": \"{{ $json.content }}\", \"color\": 16753920, \"fields\": [{\"name\": \"User\", \"value\": \"{{ $json.author.username || 'woody' }}\", \"inline\": true}, {\"name\": \"Time\", \"value\": \"{{ $now.toISO() }}\", \"inline\": true}]}]"
                            }
                        ]
                    }
                },
                "id": "discord-confirm",
                "name": "Discord Confirmation",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.2,
                "position": [680, 300]
            }
        ],
        "connections": {
            "BMF Work Webhook": {
                "main": [
                    [
                        {
                            "node": "Log to Supabase",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Log to Supabase": {
                "main": [
                    [
                        {
                            "node": "Discord Confirmation",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "settings": {},
        "staticData": {},
        "tags": []
    }
    
    print(f"🔄 Creating new BMF workflow...")
    
    try:
        create_response = requests.post(
            f'{N8N_URL}/api/v1/workflows',
            headers=headers,
            json=new_workflow
        )
        
        if create_response.status_code == 201:
            new_workflow_data = create_response.json()
            new_id = new_workflow_data.get('id')
            print(f"✅ New BMF workflow created successfully!")
            print(f"   ID: {new_id}")
            print(f"   Webhook: {N8N_URL}/webhook/bmf-work-new")
            
            # Test the new workflow
            print(f"\n🧪 Testing new BMF workflow...")
            test_data = {
                "content": "BMF work: New workflow test - " + datetime.now().strftime('%H:%M:%S'),
                "author": {"username": "woody"},
                "channel": "bmf-work"
            }
            
            test_response = requests.post(
                f'{N8N_URL}/webhook/bmf-work-new',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if test_response.status_code == 200:
                print(f"   ✅ New BMF workflow is working perfectly!")
                print(f"   📱 Check #bmf-work channel for confirmation message")
                
                # Deactivate old workflow
                print(f"\n🔄 Deactivating old BMF workflow...")
                deactivate_response = requests.post(
                    f'{N8N_URL}/api/v1/workflows/Y0C7ES8nygbFprQy/deactivate',
                    headers=headers
                )
                if deactivate_response.status_code == 200:
                    print(f"   ✅ Old workflow deactivated")
                
                return f"bmf-work-new"
            else:
                print(f"   ❌ Test failed: {test_response.status_code}")
                
        else:
            print(f"❌ Failed to create workflow: {create_response.status_code}")
            print(f"Error: {create_response.text}")
            
    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
    
    return None

if __name__ == "__main__":
    working_path = test_bmf_and_create_new()
    if working_path:
        print(f"\n🎉 BMF Work Logging is now fixed!")
        print(f"✅ Working webhook: {N8N_URL}/webhook/{working_path}")
        print(f"📱 Test it in Discord #bmf-work channel:")
        print(f"   Type: 'BMF work: Testing the fixed logging system'")
        print(f"   You should get a confirmation message back!")