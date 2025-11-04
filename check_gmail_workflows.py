import requests
import json

# n8n API configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

GMAIL_WF_IDS = ["qAobPItoZSgelYHn", "wnvzXLgk0W75yC4j"]

print("=" * 80)
print("GMAIL ORGANIZATION WORKFLOW STATUS")
print("=" * 80)

for wf_id in GMAIL_WF_IDS:
    print(f"\nWorkflow ID: {wf_id}")
    print("-" * 80)

    response = requests.get(f"{N8N_URL}/api/v1/workflows/{wf_id}", headers=headers)

    if response.status_code == 200:
        workflow = response.json()

        print(f"Name: {workflow['name']}")
        print(f"Active: {workflow.get('active', False)}")
        print(f"Created: {workflow.get('createdAt', 'Unknown')}")
        print(f"Updated: {workflow.get('updatedAt', 'Unknown')}")
        print(f"Nodes: {len(workflow.get('nodes', []))}")

        # Check for triggers
        triggers = []
        for node in workflow.get('nodes', []):
            node_type = node.get('type', '')
            if 'trigger' in node_type.lower() or 'schedule' in node_type.lower():
                triggers.append({
                    'name': node['name'],
                    'type': node_type,
                    'params': node.get('parameters', {})
                })

        print(f"\nTriggers: {len(triggers)}")
        for t in triggers:
            print(f"  - {t['name']} ({t['type']})")
            if 'rule' in t['params']:
                print(f"    Schedule: {t['params'].get('rule', {})}")

        # Check credentials
        creds_used = set()
        for node in workflow.get('nodes', []):
            if 'credentials' in node:
                for cred_type in node['credentials']:
                    creds_used.add(cred_type)

        print(f"\nCredentials Used: {', '.join(creds_used) if creds_used else 'None'}")

        # Check for Gmail nodes
        gmail_nodes = [n for n in workflow.get('nodes', []) if 'gmail' in n.get('type', '').lower()]
        print(f"Gmail Nodes: {len(gmail_nodes)}")
        for gn in gmail_nodes:
            print(f"  - {gn['name']} ({gn['type']})")

        # Check for Discord/notification nodes
        notify_nodes = [n for n in workflow.get('nodes', []) if 'discord' in n.get('name', '').lower() or 'http' in n.get('type', '').lower()]
        print(f"Notification Nodes: {len(notify_nodes)}")

    else:
        print(f"[ERROR] Could not get workflow: {response.status_code}")

print("\n" + "=" * 80)
print("RECOMMENDATION")
print("=" * 80)

# Get executions for both
print("\nChecking recent executions...")
for wf_id in GMAIL_WF_IDS:
    exec_response = requests.get(
        f"{N8N_URL}/api/v1/executions",
        headers=headers,
        params={'workflowId': wf_id, 'limit': 5}
    )

    if exec_response.status_code == 200:
        executions = exec_response.json()['data']
        print(f"\nWorkflow {wf_id}: {len(executions)} recent executions")
        if executions:
            latest = executions[0]
            print(f"  Latest: {latest['status']} at {latest.get('startedAt', 'Unknown')}")

print("\n" + "=" * 80)
print("\nYou have 2 identical workflows. This might cause issues.")
print("Recommend: Keep the newer one, deactivate the older one.")
print("=" * 80)
