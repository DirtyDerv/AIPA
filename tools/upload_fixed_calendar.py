import requests
import json

# n8n API configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

CALENDAR_WF_ID = "JG4cI6JJErOgPenc"

print("Uploading fixed Calendar Management workflow...\n")

# Read the fixed workflow
with open('n8n-workflows/06-calendar-management.json', 'r', encoding='utf-8') as f:
    workflow_data = json.load(f)

# First, get the current workflow to preserve credentials
print("Getting current workflow...")
response = requests.get(f"{N8N_URL}/api/v1/workflows/{CALENDAR_WF_ID}", headers=headers)

if response.status_code == 200:
    current_wf = response.json()

    # Preserve the credential references from current workflow
    print("Preserving credential references...")

    # Map nodes by ID to update credentials
    current_nodes = {node['id']: node for node in current_wf.get('nodes', [])}

    for node in workflow_data['nodes']:
        node_id = node.get('id')
        if node_id in current_nodes:
            current_node = current_nodes[node_id]
            # Preserve credentials if they exist
            if 'credentials' in current_node:
                node['credentials'] = current_node['credentials']

    # Prepare update
    update_data = {
        'name': workflow_data['name'],
        'nodes': workflow_data['nodes'],
        'connections': workflow_data['connections'],
        'settings': workflow_data.get('settings', {}),
        'staticData': current_wf.get('staticData')
    }

    # Update the workflow
    print(f"Updating workflow {CALENDAR_WF_ID}...")
    update_response = requests.put(
        f"{N8N_URL}/api/v1/workflows/{CALENDAR_WF_ID}",
        headers=headers,
        json=update_data
    )

    if update_response.status_code == 200:
        print("[OK] Successfully updated Calendar Management workflow!")
        print("\nFixed issue: SQL query expression syntax in 'Check for Conflicts' node")
    else:
        print(f"[FAIL] Failed to update: {update_response.status_code}")
        print(f"Response: {update_response.text}")
else:
    print(f"[FAIL] Failed to get current workflow: {response.status_code}")
    print(f"Response: {response.text}")
