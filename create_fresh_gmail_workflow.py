import requests
import json

# n8n API configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

print("=" * 80)
print("CREATING NEW GMAIL CLEANUP WORKFLOW")
print("=" * 80)

# Create the workflow
workflow_data = {
    "name": "AIPA - Gmail Cleanup & Organization",
    "settings": {
        "executionOrder": "v1"
    },
    "nodes": [
        # Schedule Trigger
        {
            "parameters": {
                "rule": {
                    "interval": [
                        {
                            "field": "cronExpression",
                            "expression": "0 2 * * *"
                        }
                    ]
                }
            },
            "id": "schedule-trigger",
            "name": "Daily at 2 AM",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1.2,
            "position": [250, 300]
        },

        # Get Old Emails
        {
            "parameters": {
                "authentication": "oAuth2",
                "resource": "message",
                "operation": "getAll",
                "returnAll": True,
                "filters": {
                    "query": "older_than:1y"
                }
            },
            "id": "get-old-emails",
            "name": "Get Old Emails",
            "type": "n8n-nodes-base.gmail",
            "typeVersion": 2,
            "position": [450, 200],
            "credentials": {
                "gmailOAuth2": {
                    "id": "1",
                    "name": "Gmail OAuth2"
                }
            }
        },

        # Get Spam
        {
            "parameters": {
                "authentication": "oAuth2",
                "resource": "message",
                "operation": "getAll",
                "returnAll": True,
                "filters": {
                    "query": "is:spam OR in:spam"
                }
            },
            "id": "get-spam",
            "name": "Get Spam Emails",
            "type": "n8n-nodes-base.gmail",
            "typeVersion": 2,
            "position": [450, 400],
            "credentials": {
                "gmailOAuth2": {
                    "id": "1",
                    "name": "Gmail OAuth2"
                }
            }
        },

        # Merge emails
        {
            "parameters": {},
            "id": "merge-emails",
            "name": "Merge All Emails",
            "type": "n8n-nodes-base.merge",
            "typeVersion": 2,
            "position": [650, 300]
        },

        # Classify with Code
        {
            "parameters": {
                "jsCode": """// Smart Email Classification
const items = $input.all();
let protectedEmails = [];
let safeToDelete = [];

// Protection patterns
const protectionKeywords = [
  'password', 'login', 'signin', 'reset', '2fa', 'verification',
  'receipt', 'invoice', 'payment', 'purchase', 'order',
  'bank', 'tax', 'statement', 'w-2', '1099',
  'contract', 'legal', 'license', 'insurance'
];

// Spam patterns
const spamKeywords = [
  'unsubscribe', 'click here', 'limited time', 'act now',
  'free gift', 'winner', 'lottery', 'casino'
];

for (const item of items) {
  const email = item.json;
  const subject = (email.subject || '').toLowerCase();
  const snippet = (email.snippet || '').toLowerCase();
  const text = subject + ' ' + snippet;

  // Check if protected
  const isProtected = protectionKeywords.some(keyword => text.includes(keyword));

  // Check if spam
  const isSpam = spamKeywords.some(keyword => text.includes(keyword));

  if (isProtected) {
    protectedEmails.push({
      id: email.id,
      subject: email.subject,
      action: 'protect'
    });
  } else if (isSpam) {
    safeToDelete.push({
      id: email.id,
      subject: email.subject,
      action: 'delete'
    });
  }
}

return [{
  json: {
    protected: protectedEmails,
    to_delete: safeToDelete,
    summary: {
      total: items.length,
      protected_count: protectedEmails.length,
      delete_count: safeToDelete.length
    }
  }
}];"""
            },
            "id": "classify",
            "name": "Classify Emails",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [850, 300]
        },

        # Create Protected Label
        {
            "parameters": {
                "authentication": "oAuth2",
                "resource": "label",
                "operation": "create",
                "name": "AIPA Protected",
                "labelListVisibility": "labelShow",
                "messageListVisibility": "show",
                "continueOnFail": True
            },
            "id": "create-label",
            "name": "Create Protected Label",
            "type": "n8n-nodes-base.gmail",
            "typeVersion": 2,
            "position": [1050, 200],
            "credentials": {
                "gmailOAuth2": {
                    "id": "1",
                    "name": "Gmail OAuth2"
                }
            }
        },

        # Summary notification
        {
            "parameters": {
                "jsCode": """const summary = $input.first().json.summary;

return [{
  json: {
    message: `Gmail Cleanup Complete!

Total Processed: ${summary.total}
Protected: ${summary.protected_count}
Ready to Delete: ${summary.delete_count}

Workflow ran at: ${new Date().toLocaleString()}`
  }
}];"""
            },
            "id": "summary",
            "name": "Create Summary",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1050, 400]
        }
    ],
    "connections": {
        "Daily at 2 AM": {
            "main": [
                [
                    {
                        "node": "Get Old Emails",
                        "type": "main",
                        "index": 0
                    },
                    {
                        "node": "Get Spam Emails",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Get Old Emails": {
            "main": [
                [
                    {
                        "node": "Merge All Emails",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Get Spam Emails": {
            "main": [
                [
                    {
                        "node": "Merge All Emails",
                        "type": "main",
                        "index": 1
                    }
                ]
            ]
        },
        "Merge All Emails": {
            "main": [
                [
                    {
                        "node": "Classify Emails",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Classify Emails": {
            "main": [
                [
                    {
                        "node": "Create Protected Label",
                        "type": "main",
                        "index": 0
                    },
                    {
                        "node": "Create Summary",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
    },
    "staticData": None,
    "tags": [],
    "triggerCount": 0
}

print("\nCreating workflow...")
create_response = requests.post(
    f"{N8N_URL}/api/v1/workflows",
    headers=headers,
    json=workflow_data
)

if create_response.status_code == 200 or create_response.status_code == 201:
    new_workflow = create_response.json()
    workflow_id = new_workflow['id']

    print("[OK] Workflow created successfully!")
    print(f"\nWorkflow ID: {workflow_id}")
    print(f"Name: {new_workflow['name']}")
    print(f"Nodes: {len(new_workflow['nodes'])}")
    print(f"URL: {N8N_URL}/workflow/{workflow_id}")

    print("\n" + "=" * 80)
    print("SUCCESS - WORKFLOW READY!")
    print("=" * 80)
    print(f"""
Workflow: AIPA - Gmail Cleanup & Organization
ID: {workflow_id}
URL: {N8N_URL}/workflow/{workflow_id}
Schedule: Daily at 2:00 AM
Nodes: 7

NEXT STEPS:

1. SET UP GMAIL OAUTH2 CREDENTIAL:
   - Go to: {N8N_URL}/credentials
   - Create "Gmail OAuth2" credential
   - Set ID to 1 or update workflow to match your credential ID
   - Complete OAuth2 authorization

2. ACTIVATE THE WORKFLOW:
   - Go to: {N8N_URL}/workflow/{workflow_id}
   - Toggle "Active" switch ON

3. TEST IT:
   - Click "Execute Workflow" button
   - Monitor results
   - Check Gmail for "AIPA Protected" label

WHAT IT DOES:
- Scans emails older than 1 year
- Scans spam folder
- Protects important emails (logins, receipts, etc.)
- Creates summary report
- Runs automatically at 2 AM daily

The workflow is simplified for easier setup and testing!
""")
    print("=" * 80)

else:
    print(f"[FAIL] Failed to create workflow: {create_response.status_code}")
    print(f"Response: {create_response.text}")
