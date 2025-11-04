import requests
import json

# n8n API configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

BI_WF_ID = "l4fNYmAfBcN2t4YQ"

print("Adding Execute Workflow Trigger to Business Intelligence & Reports workflow...\n")

# Get the current workflow
response = requests.get(f"{N8N_URL}/api/v1/workflows/{BI_WF_ID}", headers=headers)

if response.status_code == 200:
    workflow = response.json()

    print(f"Current workflow: {workflow.get('name', 'Unknown')}")
    print(f"Current nodes: {len(workflow.get('nodes', []))}")

    # Check if Execute Workflow Trigger already exists
    has_trigger = any(n.get('type') == 'n8n-nodes-base.executeWorkflowTrigger' for n in workflow.get('nodes', []))

    if has_trigger:
        print("[INFO] Execute Workflow Trigger already exists!")
    else:
        print("[INFO] Adding Execute Workflow Trigger node...")

        # Find the first non-trigger node to connect to
        first_node = None
        for node in workflow.get('nodes', []):
            node_type = node.get('type', '')
            if not node_type.endswith('Trigger'):
                first_node = node
                break

        # Create the Execute Workflow Trigger node
        trigger_node = {
            "parameters": {},
            "id": "execute-workflow-trigger",
            "name": "Execute Workflow Trigger",
            "type": "n8n-nodes-base.executeWorkflowTrigger",
            "typeVersion": 1,
            "position": [250, 300]
        }

        # Add the node
        workflow['nodes'].insert(0, trigger_node)

        # Update connections if there's a first node to connect to
        if first_node:
            if 'connections' not in workflow:
                workflow['connections'] = {}

            workflow['connections']['Execute Workflow Trigger'] = {
                "main": [
                    [
                        {
                            "node": first_node['name'],
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
            print(f"[INFO] Connected trigger to: {first_node['name']}")

        # Prepare update
        update_data = {
            'name': workflow['name'],
            'nodes': workflow['nodes'],
            'connections': workflow['connections'],
            'settings': workflow.get('settings', {}),
            'staticData': workflow.get('staticData')
        }

        # Update the workflow
        print(f"\nUploading updated workflow...")
        update_response = requests.put(
            f"{N8N_URL}/api/v1/workflows/{BI_WF_ID}",
            headers=headers,
            json=update_data
        )

        if update_response.status_code == 200:
            print("[OK] Successfully added Execute Workflow Trigger!")
        else:
            print(f"[FAIL] Failed to update: {update_response.status_code}")
            print(f"Response: {update_response.text}")
else:
    print(f"[FAIL] Failed to get workflow: {response.status_code}")
