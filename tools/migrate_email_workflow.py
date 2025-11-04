#!/usr/bin/env python3
"""
AIPA Email Processing Migration - Telegram to Discord
Converts the Email Processing workflow from Telegram to Discord webhooks
"""

import requests
import json
from datetime import datetime

# n8n Configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

# Original workflow ID
ORIGINAL_WORKFLOW_ID = "dsYFoJPM2wUqZaK3"

def get_original_workflow():
    """Get the original Telegram email workflow"""
    try:
        response = requests.get(f"{N8N_URL}/api/v1/workflows/{ORIGINAL_WORKFLOW_ID}", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get original workflow: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def create_discord_email_workflow():
    """Create Discord version of email processing workflow"""
    
    # Discord webhook URLs for email notifications
    email_alerts_webhook = "https://discord.com/api/webhooks/1434598876500852847/XYGBBPUycaoufGhBa2gnxPBeVmi3OZ0Xvk3sWH1m1-3qFp3cax2LnraJ-ofSLXilLXGc"
    
    workflow = {
        "name": "AIPA - Email Processing with AI (Discord)",
        "nodes": [
            {
                "id": "gmail-trigger",
                "name": "Gmail Trigger - Check New Emails",
                "type": "n8n-nodes-base.gmailTrigger",
                "typeVersion": 1,
                "position": [200, 300],
                "parameters": {
                    "pollTimes": {
                        "item": [
                            {
                                "mode": "everyMinute"
                            }
                        ]
                    },
                    "labelIds": ["INBOX"],
                    "simple": False
                },
                "credentials": {
                    "gmailOAuth2": {
                        "id": "1",
                        "name": "AIPA Gmail"
                    }
                }
            },
            {
                "id": "parse-email",
                "name": "Parse Email Data",
                "type": "n8n-nodes-base.function",
                "typeVersion": 1,
                "position": [400, 300],
                "parameters": {
                    "functionCode": "// Extract email details for AI classification\nconst emailData = {\n  from: $json.payload.headers.find(h => h.name === 'From')?.value || 'Unknown',\n  subject: $json.payload.headers.find(h => h.name === 'Subject')?.value || 'No Subject',\n  snippet: $json.snippet || '',\n  threadId: $json.threadId,\n  messageId: $json.id,\n  receivedDate: new Date().toISOString()\n};\n\n// Clean and prepare text for AI\nconst cleanText = (emailData.subject + ' ' + emailData.snippet)\n  .replace(/[\\r\\n]+/g, ' ')\n  .replace(/\\s+/g, ' ')\n  .trim();\n\nreturn {\n  emailData,\n  cleanText,\n  aiPrompt: `Classify this email into one of these business contexts:\n- woodys-creations: Woody's Creations UK (laser-cut gifts, custom orders)\n- dj-business: DJ services and event bookings\n- bmf-work: BMF contract work\n- the-top-odd: The Top Odd pub management\n- personal: Personal matters\n\nEmail: ${cleanText}\n\nRespond with just the business context name.`\n};"
                }
            },
            {
                "id": "ai-classify",
                "name": "AI Classify Email (Gemini)",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4,
                "position": [600, 300],
                "parameters": {
                    "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                    "method": "POST",
                    "sendHeaders": true,
                    "headerParameters": {
                        "parameters": [
                            {
                                "name": "Content-Type",
                                "value": "application/json"
                            }
                        ]
                    },
                    "sendQuery": true,
                    "queryParameters": {
                        "parameters": [
                            {
                                "name": "key",
                                "value": "AIzaSyC4W8JJfqUt-_6sTfn1GVQ3BKQ4QXZgY2k"
                            }
                        ]
                    },
                    "sendBody": true,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "contents",
                                "value": "=[{\"parts\":[{\"text\":\"{{ $json.aiPrompt }}\"}]}]"
                            }
                        ]
                    }
                }
            },
            {
                "id": "parse-classification",
                "name": "Parse AI Classification",
                "type": "n8n-nodes-base.function",
                "typeVersion": 1,
                "position": [800, 300],
                "parameters": {
                    "functionCode": "// Parse Gemini response\nconst response = $json.candidates[0].content.parts[0].text.toLowerCase().trim();\n\n// Map classification to business context\nlet businessContext = 'personal'; // default\nif (response.includes('woodys-creations')) businessContext = 'woodys-creations';\nelse if (response.includes('dj-business')) businessContext = 'dj-business';\nelse if (response.includes('bmf-work')) businessContext = 'bmf-work';\nelse if (response.includes('the-top-odd')) businessContext = 'the-top-odd';\n\n// Check if email needs response (contains questions or requests)\nconst emailText = $node['Parse Email Data'].json.cleanText.toLowerCase();\nconst needsResponse = emailText.includes('?') || \n                     emailText.includes('please') || \n                     emailText.includes('request') || \n                     emailText.includes('quote') || \n                     emailText.includes('booking');\n\nreturn {\n  ...($node['Parse Email Data'].json),\n  businessContext,\n  classification: response,\n  needsResponse,\n  priority: needsResponse ? 'high' : 'normal'\n};"
                }
            },
            {
                "id": "label-email",
                "name": "Apply Gmail Label",
                "type": "n8n-nodes-base.gmail",
                "typeVersion": 2,
                "position": [1000, 300],
                "parameters": {
                    "operation": "addLabels",
                    "messageId": "={{ $json.emailData.messageId }}",
                    "labelIds": "={{ $json.businessContext === 'woodys-creations' ? ['Label_1'] : $json.businessContext === 'dj-business' ? ['Label_2'] : $json.businessContext === 'bmf-work' ? ['Label_3'] : $json.businessContext === 'the-top-odd' ? ['Label_4'] : ['Label_5'] }}"
                },
                "credentials": {
                    "gmailOAuth2": {
                        "id": "1",
                        "name": "AIPA Gmail"
                    }
                }
            },
            {
                "id": "save-to-database",
                "name": "Save Email to Database",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4,
                "position": [1200, 300],
                "parameters": {
                    "url": "https://neoeoabqcfpopzkwvcxq.supabase.co/rest/v1/conversations",
                    "method": "POST",
                    "sendHeaders": true,
                    "headerParameters": {
                        "parameters": [
                            {
                                "name": "apikey",
                                "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck"
                            },
                            {
                                "name": "Authorization",
                                "value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck"
                            },
                            {
                                "name": "Content-Type",
                                "value": "application/json"
                            }
                        ]
                    },
                    "sendBody": true,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "user_id",
                                "value": "={{ $json.emailData.from }}"
                            },
                            {
                                "name": "message",
                                "value": "={{ $json.emailData.subject + ': ' + $json.emailData.snippet }}"
                            },
                            {
                                "name": "business_context",
                                "value": "={{ $json.businessContext }}"
                            },
                            {
                                "name": "created_at",
                                "value": "={{ $json.emailData.receivedDate }}"
                            },
                            {
                                "name": "metadata",
                                "value": "={{ JSON.stringify({messageId: $json.emailData.messageId, threadId: $json.emailData.threadId, classification: $json.classification, priority: $json.priority}) }}"
                            }
                        ]
                    }
                }
            },
            {
                "id": "check-needs-response",
                "name": "Check if Needs Response",
                "type": "n8n-nodes-base.if",
                "typeVersion": 1,
                "position": [1400, 300],
                "parameters": {
                    "conditions": {
                        "boolean": [
                            {
                                "value1": "={{ $json.needsResponse }}",
                                "value2": true
                            }
                        ]
                    }
                }
            },
            {
                "id": "generate-response",
                "name": "Generate Draft Response (Gemini)",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4,
                "position": [1600, 200],
                "parameters": {
                    "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                    "method": "POST",
                    "sendHeaders": true,
                    "headerParameters": {
                        "parameters": [
                            {
                                "name": "Content-Type",
                                "value": "application/json"
                            }
                        ]
                    },
                    "sendQuery": true,
                    "queryParameters": {
                        "parameters": [
                            {
                                "name": "key",
                                "value": "AIzaSyC4W8JJfqUt-_6sTfn1GVQ3BKQ4QXZgY2k"
                            }
                        ]
                    },
                    "sendBody": true,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "contents",
                                "value": "=[{\"parts\":[{\"text\":\"Generate a professional email response for business context: {{ $json.businessContext }}\\n\\nOriginal email: {{ $json.emailData.subject }} - {{ $json.emailData.snippet }}\\n\\nWrite a helpful, professional response.\"}]}]"
                            }
                        ]
                    }
                }
            },
            {
                "id": "create-gmail-draft",
                "name": "Create Gmail Draft",
                "type": "n8n-nodes-base.gmail",
                "typeVersion": 2,
                "position": [1800, 200],
                "parameters": {
                    "operation": "draft",
                    "message": {
                        "to": "={{ $node['Parse AI Classification'].json.emailData.from }}",
                        "subject": "Re: {{ $node['Parse AI Classification'].json.emailData.subject }}",
                        "body": "={{ $json.candidates[0].content.parts[0].text }}",
                        "replyToMessageId": "={{ $node['Parse AI Classification'].json.emailData.messageId }}"
                    }
                },
                "credentials": {
                    "gmailOAuth2": {
                        "id": "1",
                        "name": "AIPA Gmail"
                    }
                }
            },
            {
                "id": "discord-high-priority",
                "name": "Discord Alert - High Priority",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4,
                "position": [2000, 200],
                "parameters": {
                    "url": email_alerts_webhook,
                    "method": "POST",
                    "sendHeaders": true,
                    "headerParameters": {
                        "parameters": [
                            {
                                "name": "Content-Type",
                                "value": "application/json"
                            }
                        ]
                    },
                    "sendBody": true,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "embeds",
                                "value": "=[{\"title\":\"🚨 High Priority Email - Response Needed\",\"description\":\"{{ $node['Parse AI Classification'].json.emailData.subject }}\",\"color\":15158332,\"fields\":[{\"name\":\"📧 From\",\"value\":\"{{ $node['Parse AI Classification'].json.emailData.from }}\",\"inline\":true},{\"name\":\"🏢 Business\",\"value\":\"{{ $node['Parse AI Classification'].json.businessContext }}\",\"inline\":true},{\"name\":\"📄 Preview\",\"value\":\"{{ $node['Parse AI Classification'].json.emailData.snippet.substring(0,200) }}...\"},{\"name\":\"📝 Action Required\",\"value\":\"Draft response created in Gmail - Review and send\"}],\"timestamp\":\"{{ new Date().toISOString() }}\"}]"
                            }
                        ]
                    }
                }
            },
            {
                "id": "discord-info-only",
                "name": "Discord Alert - Info Only",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4,
                "position": [1600, 400],
                "parameters": {
                    "url": email_alerts_webhook,
                    "method": "POST",
                    "sendHeaders": true,
                    "headerParameters": {
                        "parameters": [
                            {
                                "name": "Content-Type",
                                "value": "application/json"
                            }
                        ]
                    },
                    "sendBody": true,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "embeds",
                                "value": "=[{\"title\":\"📬 New Email Processed\",\"description\":\"{{ $json.emailData.subject }}\",\"color\":3447003,\"fields\":[{\"name\":\"📧 From\",\"value\":\"{{ $json.emailData.from }}\",\"inline\":true},{\"name\":\"🏢 Business\",\"value\":\"{{ $json.businessContext }}\",\"inline\":true},{\"name\":\"📄 Preview\",\"value\":\"{{ $json.emailData.snippet.substring(0,200) }}...\"}],\"timestamp\":\"{{ new Date().toISOString() }}\"}]"
                            }
                        ]
                    }
                }
            }
        ],
        "connections": {
            "gmail-trigger": {
                "main": [
                    [
                        {
                            "node": "parse-email",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "parse-email": {
                "main": [
                    [
                        {
                            "node": "ai-classify",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "ai-classify": {
                "main": [
                    [
                        {
                            "node": "parse-classification",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "parse-classification": {
                "main": [
                    [
                        {
                            "node": "label-email",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "label-email": {
                "main": [
                    [
                        {
                            "node": "save-to-database",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "save-to-database": {
                "main": [
                    [
                        {
                            "node": "check-needs-response",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "check-needs-response": {
                "main": [
                    [
                        {
                            "node": "generate-response",
                            "type": "main",
                            "index": 0
                        }
                    ],
                    [
                        {
                            "node": "discord-info-only",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "generate-response": {
                "main": [
                    [
                        {
                            "node": "create-gmail-draft",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "create-gmail-draft": {
                "main": [
                    [
                        {
                            "node": "discord-high-priority",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "active": false,
        "settings": {
            "executionOrder": "v1"
        },
        "versionId": "1"
    }
    
    return workflow

def create_workflow():
    """Create the Discord-enabled email workflow"""
    print("🚀 Creating Discord Email Processing Workflow")
    print("=" * 50)
    
    # Get original workflow for reference
    original = get_original_workflow()
    if original:
        print(f"✅ Found original workflow: {original['name']}")
    
    # Create new Discord workflow
    discord_workflow = create_discord_email_workflow()
    
    try:
        response = requests.post(f"{N8N_URL}/api/v1/workflows", headers=headers, json=discord_workflow)
        
        if response.status_code == 201:
            new_workflow = response.json()
            print(f"✅ Created Discord workflow!")
            print(f"   📋 Name: {new_workflow['name']}")
            print(f"   🆔 ID: {new_workflow['id']}")
            print(f"   📊 Nodes: {len(new_workflow['nodes'])}")
            
            print(f"\n🔄 Migration Changes Made:")
            print(f"   • Replaced Telegram notifications → Discord rich embeds")
            print(f"   • Added color-coded priority levels")
            print(f"   • Enhanced email preview formatting")
            print(f"   • Maintained all AI classification logic")
            print(f"   • Kept Gmail labeling and database saving")
            
            print(f"\n📋 Next Steps:")
            print(f"   1. Test the new Discord workflow")
            print(f"   2. Verify Discord notifications appear correctly")
            print(f"   3. Deactivate original Telegram workflow")
            print(f"   4. Activate Discord workflow")
            
            return new_workflow['id']
            
        else:
            print(f"❌ Failed to create workflow: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
        return None

if __name__ == "__main__":
    workflow_id = create_workflow()
    if workflow_id:
        print(f"\n🎉 Discord email workflow created successfully!")
        print(f"🆔 New Workflow ID: {workflow_id}")
    else:
        print(f"\n❌ Failed to create Discord email workflow")