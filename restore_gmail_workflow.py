import requests
import json

# n8n API configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

GMAIL_WF_ID = "wnvzXLgk0W75yC4j"

print("=" * 80)
print("RESTORING GMAIL CLEANUP WORKFLOW FROM ARCHIVE")
print("=" * 80)

# Step 1: Get the archived workflow
print("\n[Step 1] Getting archived workflow...")
print("-" * 80)

response = requests.get(f"{N8N_URL}/api/v1/workflows/{GMAIL_WF_ID}", headers=headers)

if response.status_code != 200:
    print(f"[ERROR] Could not get workflow: {response.status_code}")
    print(f"Response: {response.text}")
    exit(1)

workflow = response.json()
print(f"[OK] Found: {workflow['name']}")
print(f"Status: Active={workflow.get('active', False)}, Archived={workflow.get('isArchived', False)}")
print(f"Nodes: {len(workflow['nodes'])}")

# Step 2: Unarchive the workflow
print("\n[Step 2] Unarchiving workflow...")
print("-" * 80)

# Update to unarchive
update_data = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections'],
    'settings': workflow.get('settings', {}),
    'staticData': workflow.get('staticData')
}

# Note: n8n API might not support directly setting isArchived, so we just update normally
update_response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{GMAIL_WF_ID}",
    headers=headers,
    json=update_data
)

if update_response.status_code == 200:
    print("[OK] Workflow updated")
else:
    print(f"[INFO] Update response: {update_response.status_code}")

# Step 3: Add schedule trigger if missing
print("\n[Step 3] Checking for schedule trigger...")
print("-" * 80)

has_schedule = False
for node in workflow['nodes']:
    if 'schedule' in node.get('type', '').lower() or 'cron' in node.get('type', '').lower():
        has_schedule = True
        print(f"[OK] Found trigger: {node['name']}")
        break

if not has_schedule:
    print("[ACTION] Adding schedule trigger...")

    # Create schedule trigger
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
        "id": "gmail-schedule-trigger",
        "name": "Daily at 2 AM",
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.2,
        "position": [250, 300]
    }

    workflow['nodes'].insert(0, schedule_node)

    # Find first non-trigger node to connect
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

# Step 4: Configure credentials
print("\n[Step 4] Configuring credentials...")
print("-" * 80)

# Use correct credential IDs from earlier
CRED_MAP = {
    "gmailOAuth2": {"id": "1", "name": "Gmail OAuth2"},
    "supabaseApi": {"id": "yIakFUgoeTPS1z3R", "name": "Supabase account"}
}

gmail_node_count = 0
for node in workflow['nodes']:
    node_type = node.get('type', '')

    # Gmail nodes
    if 'gmail' in node_type.lower():
        if 'credentials' not in node:
            node['credentials'] = {}
        node['credentials']['gmailOAuth2'] = CRED_MAP['gmailOAuth2']
        gmail_node_count += 1
        print(f"  Added Gmail creds to: {node['name']}")

    # Supabase nodes
    if 'supabase' in node_type.lower():
        if 'credentials' not in node:
            node['credentials'] = {}
        node['credentials']['supabaseApi'] = CRED_MAP['supabaseApi']
        print(f"  Added Supabase creds to: {node['name']}")

print(f"[OK] Configured credentials for {gmail_node_count} Gmail nodes")

# Step 5: Update workflow
print("\n[Step 5] Uploading restored workflow...")
print("-" * 80)

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
    print("[OK] Workflow restored and updated!")
else:
    print(f"[FAIL] Update failed: {update_response.status_code}")
    print(f"Response: {update_response.text}")
    exit(1)

# Step 6: Summary
print("\n" + "=" * 80)
print("RESTORATION COMPLETE")
print("=" * 80)
print(f"""
Workflow: {workflow['name']}
ID: {GMAIL_WF_ID}
URL: http://192.168.0.14:5678/workflow/{GMAIL_WF_ID}
Nodes: {len(workflow['nodes'])}
Gmail Nodes: {gmail_node_count}

IMPORTANT - MANUAL STEPS:

1. UNARCHIVE THE WORKFLOW IN UI:
   - Go to: http://192.168.0.14:5678/workflows
   - Click on the workflow
   - Look for "Unarchive" option
   - OR the workflow may already be unarchived

2. SET UP GMAIL OAUTH2 CREDENTIALS:
   - Go to: http://192.168.0.14:5678/credentials
   - Create "Gmail OAuth2" credential (if not exists)
   - Complete OAuth2 setup
   - The workflow expects credential ID: 1

3. ACTIVATE THE WORKFLOW:
   - Open: http://192.168.0.14:5678/workflow/{GMAIL_WF_ID}
   - Toggle "Active" switch ON

4. TEST EXECUTION:
   - Click "Execute Workflow" button
   - Monitor results

WHAT IT DOES:
- Runs daily at 2:00 AM
- Scans emails older than 1 year
- Protects important emails (logins, receipts, legal)
- Creates organized Gmail labels
- Safely deletes confirmed spam/junk
- Logs all operations to Supabase

""")
print("=" * 80)
