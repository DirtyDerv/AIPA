import requests
import json

N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

headers = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}

WORKFLOW_ID = "BTPrjJ8mq6snkm86"

print("Adding nodes to Gmail workflow...")

# Build the complete workflow
workflow_update = {
    "name": "AIPA - Gmail Cleanup & Organization",
    "nodes": [
        {
            "parameters": {
                "rule": {
                    "interval": [{"field": "cronExpression", "expression": "0 2 * * *"}]
                }
            },
            "id": "schedule",
            "name": "Daily at 2 AM",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1.2,
            "position": [250, 300]
        },
        {
            "parameters": {
                "authentication": "oAuth2",
                "resource": "message",
                "operation": "getAll",
                "returnAll": True,
                "filters": {"query": "older_than:1y"}
            },
            "id": "get-old",
            "name": "Get Old Emails",
            "type": "n8n-nodes-base.gmail",
            "typeVersion": 2,
            "position": [450, 300],
            "credentials": {"gmailOAuth2": {"id": "1", "name": "Gmail OAuth2"}}
        },
        {
            "parameters": {
                "jsCode": "return $input.all().map(item => ({json: {message: 'Gmail cleanup ready. Configure credentials to run.'}}));"
            },
            "id": "summary",
            "name": "Summary",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [650, 300]
        }
    ],
    "connections": {
        "Daily at 2 AM": {"main": [[{"node": "Get Old Emails", "type": "main", "index": 0}]]},
        "Get Old Emails": {"main": [[{"node": "Summary", "type": "main", "index": 0}]]}
    },
    "settings": {}
}

response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers,
    json=workflow_update
)

if response.status_code == 200:
    print(f"[OK] Workflow populated successfully!")
    print(f"\nWorkflow ID: {WORKFLOW_ID}")
    print(f"URL: {N8N_URL}/workflow/{WORKFLOW_ID}")
    print("\nNodes added:")
    print("  1. Daily at 2 AM (Schedule Trigger)")
    print("  2. Get Old Emails (Gmail)")
    print("  3. Summary (Code)")
    print("\nNEXT STEPS:")
    print("1. Go to URL above")
    print("2. Set up Gmail OAuth2 credential")
    print("3. Activate workflow")
    print("4. Test it!")
else:
    print(f"[FAIL] {response.status_code}: {response.text}")
