import requests
import json
import time

# n8n API configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

# Workflows to update
workflows_to_fix = [
    {
        "file": "n8n-workflows/06-calendar-management.json",
        "id": "JG4cI6JJErOgPenc",
        "name": "Calendar Management"
    }
]

print("Updating fixed workflows...\n")
print("=" * 80)

for wf in workflows_to_fix:
    print(f"\nUpdating: {wf['name']}")
    print(f"File: {wf['file']}")
    print(f"ID: {wf['id']}")

    # Read the fixed workflow JSON
    try:
        with open(wf['file'], 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)

        # Prepare update data
        update_data = {
            'name': workflow_data['name'],
            'nodes': workflow_data['nodes'],
            'connections': workflow_data['connections'],
            'settings': workflow_data.get('settings', {}),
            'staticData': workflow_data.get('staticData')
        }

        # Update the workflow
        response = requests.put(
            f"{N8N_URL}/api/v1/workflows/{wf['id']}",
            headers=headers,
            json=update_data
        )

        if response.status_code == 200:
            print(f"[OK] Successfully updated: {wf['name']}")
        else:
            print(f"[FAIL] Failed to update {wf['name']}: {response.status_code}")
            print(f"  Response: {response.text}")

        time.sleep(2)  # Rate limit protection

    except Exception as e:
        print(f"[ERROR] Exception updating {wf['name']}: {str(e)}")

print("\n" + "=" * 80)
print("\nUpdate complete!")
