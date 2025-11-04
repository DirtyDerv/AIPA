import requests
import json

# n8n API configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

TELEGRAM_WF_ID = "DRuQZOp9tM79Sf6D"

print("Searching for Execute Workflow nodes...\n")

response = requests.get(f"{N8N_URL}/api/v1/workflows/{TELEGRAM_WF_ID}", headers=headers)

if response.status_code == 200:
    workflow = response.json()

    print(f"Workflow: {workflow.get('name', 'Unknown')}\n")

    for node in workflow.get('nodes', []):
        node_type = node.get('type', '')
        node_name = node.get('name', 'Unnamed')

        # Check for Execute Workflow nodes or nodes with "report" in the name
        if node_type == 'n8n-nodes-base.executeWorkflow' or 'report' in node_name.lower():
            print(f"Found: {node_name}")
            print(f"  Type: {node_type}")
            print(f"  Parameters:")
            print(json.dumps(node.get('parameters', {}), indent=4))
            print()
else:
    print(f"Failed to get workflow: {response.status_code}")
