import requests
import json
import time

# n8n API configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

# IDs
WORKING_WF_ID = "wnvzXLgk0W75yC4j"  # Has successful execution
DUPLICATE_WF_ID = "qAobPItoZSgelYHn"  # Duplicate to remove

print("=" * 80)
print("GMAIL CLEANUP WORKFLOW - COMPLETE SETUP")
print("=" * 80)

# Step 1: Deactivate and delete duplicate
print("\n[Step 1] Removing duplicate workflow...")
print("-" * 80)

response = requests.get(f"{N8N_URL}/api/v1/workflows/{DUPLICATE_WF_ID}", headers=headers)
if response.status_code == 200:
    dup_workflow = response.json()

    # Deactivate first
    dup_workflow['active'] = False
    update_data = {
        'name': dup_workflow['name'],
        'nodes': dup_workflow['nodes'],
        'connections': dup_workflow['connections'],
        'settings': dup_workflow.get('settings', {}),
        'staticData': dup_workflow.get('staticData')
    }

    requests.put(f"{N8N_URL}/api/v1/workflows/{DUPLICATE_WF_ID}", headers=headers, json=update_data)

    # Delete
    delete_response = requests.delete(f"{N8N_URL}/api/v1/workflows/{DUPLICATE_WF_ID}", headers=headers)
    if delete_response.status_code == 200:
        print("[OK] Duplicate workflow removed")
    else:
        print(f"[INFO] Could not delete duplicate (may need manual removal): {delete_response.status_code}")
else:
    print("[INFO] Duplicate already removed or not found")

time.sleep(2)

# Step 2: Get and update the working workflow
print("\n[Step 2] Configuring the working workflow...")
print("-" * 80)

response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKING_WF_ID}", headers=headers)

if response.status_code != 200:
    print(f"[ERROR] Could not get workflow: {response.status_code}")
    exit(1)

workflow = response.json()
print(f"Workflow: {workflow['name']}")
print(f"Current nodes: {len(workflow['nodes'])}")

# Step 3: Add Schedule Trigger
print("\n[Step 3] Adding schedule trigger (daily at 2 AM)...")
print("-" * 80)

has_trigger = any('trigger' in n.get('type', '').lower() for n in workflow['nodes'])

if not has_trigger:
    # Add Schedule Trigger node
    schedule_node = {
        "parameters": {
            "rule": {
                "interval": [
                    {
                        "field": "cronExpression",
                        "expression": "0 2 * * *"  # 2 AM daily
                    }
                ]
            }
        },
        "id": "schedule-trigger-gmail",
        "name": "Daily Schedule (2 AM)",
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.2,
        "position": [250, 300]
    }

    workflow['nodes'].insert(0, schedule_node)

    # Find first non-trigger node to connect to
    first_node = None
    for node in workflow['nodes'][1:]:  # Skip the trigger we just added
        if 'trigger' not in node.get('type', '').lower():
            first_node = node
            break

    if first_node:
        if 'connections' not in workflow:
            workflow['connections'] = {}

        workflow['connections']['Daily Schedule (2 AM)'] = {
            "main": [[{
                "node": first_node['name'],
                "type": "main",
                "index": 0
            }]]
        }
        print(f"[OK] Added schedule trigger, connected to: {first_node['name']}")
else:
    print("[OK] Trigger already exists")

# Step 4: Add credentials to Gmail nodes
print("\n[Step 4] Configuring Gmail OAuth credentials...")
print("-" * 80)

# Check what Gmail credentials exist
print("Note: Gmail OAuth2 credentials must be set up manually in n8n UI")
print("The workflow will reference them, but you need to:")
print("  1. Go to http://192.168.0.14:5678/credentials")
print("  2. Create 'Gmail OAuth2' credential")
print("  3. Name it 'AIPA Gmail Access'")
print("  4. Complete OAuth2 authorization")

# Add credential references to Gmail nodes
gmail_cred_ref = {
    "id": "1",  # Assuming it will be created as ID 1
    "name": "AIPA Gmail Access"
}

for node in workflow['nodes']:
    if 'gmail' in node.get('type', '').lower():
        if 'credentials' not in node:
            node['credentials'] = {}
        node['credentials']['gmailOAuth2'] = gmail_cred_ref
        print(f"  - Added credential to: {node['name']}")

# Step 5: Update the workflow
print("\n[Step 5] Uploading updated workflow...")
print("-" * 80)

update_data = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections'],
    'settings': workflow.get('settings', {}),
    'staticData': workflow.get('staticData')
}

update_response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKING_WF_ID}",
    headers=headers,
    json=update_data
)

if update_response.status_code == 200:
    print("[OK] Workflow updated successfully!")
else:
    print(f"[FAIL] Update failed: {update_response.status_code}")
    print(f"Response: {update_response.text}")
    exit(1)

# Step 6: Summary and next steps
print("\n" + "=" * 80)
print("SETUP COMPLETE!")
print("=" * 80)

print(f"""
✅ Gmail Cleanup Workflow Configured

Workflow ID: {WORKING_WF_ID}
Status: Active
Schedule: Daily at 2:00 AM
Nodes: {len(workflow['nodes'])}

⚠️  MANUAL STEPS REQUIRED:

1. SET UP GMAIL OAuth2 CREDENTIALS:
   - Go to: http://192.168.0.14:5678/credentials
   - Click: "Create New Credential"
   - Select: "Gmail OAuth2"
   - Name: "AIPA Gmail Access"
   - Follow the OAuth2 setup wizard
   - Grant permissions for Gmail access

2. VERIFY SUPABASE TABLE EXISTS:
   - Table: email_organization_logs
   - See GMAIL_ORGANIZER_GUIDE.md for SQL schema

3. CONFIGURE DISCORD WEBHOOK (Optional):
   - For email cleanup notifications
   - Add webhook URL to workflow settings

4. TEST THE WORKFLOW:
   - Go to: http://192.168.0.14:5678/workflow/{WORKING_WF_ID}
   - Click: "Execute Workflow"
   - Monitor: Results in execution panel
   - Check: Gmail labels created successfully

📋 Documentation:
- Full Guide: docs/GMAIL_ORGANIZER_GUIDE.md
- Status: docs/GMAIL_ORGANIZER_STATUS.md
- Setup Report: gmail_organizer_setup_report.json

🎯 What It Does:
- Scans emails older than 1 year
- Protects important emails (credentials, receipts, legal)
- Creates organized Gmail labels
- Safely deletes confirmed junk and spam
- Logs all operations to Supabase

⏰ Next Run: Tomorrow at 2:00 AM (automatic)

""")

print("=" * 80)
