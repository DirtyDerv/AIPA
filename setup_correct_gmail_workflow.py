import requests
import json

# n8n API configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

# User specified workflow ID
GMAIL_WF_ID = "qAobPItoZSgelYHn"

print("=" * 80)
print("GMAIL CLEANUP WORKFLOW SETUP")
print("=" * 80)
print(f"\nWorkflow ID: {GMAIL_WF_ID}")

# Get the workflow
print("\nFetching workflow...")
response = requests.get(f"{N8N_URL}/api/v1/workflows/{GMAIL_WF_ID}", headers=headers)

if response.status_code != 200:
    print(f"[ERROR] Could not get workflow: {response.status_code}")
    print(f"Response: {response.text}")
    exit(1)

workflow = response.json()
print(f"[OK] Found: {workflow['name']}")
print(f"Current nodes: {len(workflow['nodes'])}")
print(f"Active: {workflow.get('active', False)}")

# Check current state
has_trigger = False
trigger_node = None

for node in workflow['nodes']:
    if 'schedule' in node.get('type', '').lower() or 'trigger' in node.get('type', '').lower():
        has_trigger = True
        trigger_node = node
        print(f"\n[INFO] Found existing trigger: {node['name']}")

# Add schedule trigger if missing
if not has_trigger:
    print("\n[ACTION] Adding schedule trigger...")

    schedule_node = {
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
        "id": "gmail-cleanup-schedule",
        "name": "Daily at 2 AM",
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.2,
        "position": [250, 300]
    }

    workflow['nodes'].insert(0, schedule_node)

    # Find first non-trigger node
    first_node = None
    for node in workflow['nodes'][1:]:
        if 'trigger' not in node.get('type', '').lower():
            first_node = node
            break

    if first_node:
        if 'connections' not in workflow:
            workflow['connections'] = {}

        workflow['connections']['Daily at 2 AM'] = {
            "main": [[{
                "node": first_node['name'],
                "type": "main",
                "index": 0
            }]]
        }
        print(f"[OK] Connected trigger to: {first_node['name']}")
else:
    print("[OK] Schedule trigger already exists")

# Check and update credentials
print("\n[ACTION] Checking credentials...")

# Get list of Gmail nodes
gmail_nodes = []
for node in workflow['nodes']:
    if 'gmail' in node.get('type', '').lower():
        gmail_nodes.append(node)
        has_creds = 'credentials' in node and 'gmailOAuth2' in node.get('credentials', {})
        status = "[HAS CREDS]" if has_creds else "[NO CREDS]"
        print(f"  {status} {node['name']}")

# Update the workflow
print("\n[ACTION] Updating workflow...")

update_data = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections'],
    'settings': workflow.get('settings', {}),
    'staticData': workflow.get('staticData')
}

update_response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{GMAIL_WF_ID}",
    headers=headers,
    json=update_data
)

if update_response.status_code == 200:
    print("[OK] Workflow updated successfully!")
else:
    print(f"[FAIL] Update failed: {update_response.status_code}")
    print(f"Response: {update_response.text}")
    exit(1)

print("\n" + "=" * 80)
print("SETUP COMPLETE")
print("=" * 80)
print(f"""
Workflow: AIPA - Advanced Gmail Organization & Cleanup
ID: {GMAIL_WF_ID}
URL: http://192.168.0.14:5678/workflow/{GMAIL_WF_ID}
Schedule: Daily at 2:00 AM
Nodes: {len(workflow['nodes'])}

NEXT STEPS:

1. CONFIGURE GMAIL CREDENTIALS (if not already done):
   - Go to: http://192.168.0.14:5678/credentials
   - Add Gmail OAuth2 credential
   - Name it appropriately
   - The workflow already has {len(gmail_nodes)} Gmail nodes ready

2. TEST THE WORKFLOW:
   - Open: http://192.168.0.14:5678/workflow/{GMAIL_WF_ID}
   - Click: "Execute Workflow" button
   - Monitor: Execution results

3. VERIFY SCHEDULE:
   - Check the schedule trigger is configured for 2 AM
   - Next automatic run: Tomorrow at 2:00 AM

Documentation:
- Guide: docs/GMAIL_ORGANIZER_GUIDE.md
- Status: docs/GMAIL_ORGANIZER_STATUS.md
""")
print("=" * 80)
