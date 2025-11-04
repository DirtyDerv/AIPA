import requests
import json

# n8n API configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

GMAIL_WF_ID = "wnvzXLgk0W75yC4j"

print("=" * 80)
print("UNARCHIVING GMAIL WORKFLOW")
print("=" * 80)

# Get the workflow
print("\nGetting workflow...")
response = requests.get(f"{N8N_URL}/api/v1/workflows/{GMAIL_WF_ID}", headers=headers)

if response.status_code != 200:
    print(f"[ERROR] Could not get workflow: {response.status_code}")
    exit(1)

workflow = response.json()
print(f"[OK] Found: {workflow['name']}")
print(f"Current status: Archived={workflow.get('isArchived', False)}")

# Try to unarchive by updating the workflow
# Since the API might not have a direct unarchive endpoint, we'll update it normally
print("\nUnarchiving workflow...")

update_data = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections'],
    'settings': workflow.get('settings', {}),
    'staticData': workflow.get('staticData'),
    'active': False  # Keep inactive for now
}

update_response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{GMAIL_WF_ID}",
    headers=headers,
    json=update_data
)

if update_response.status_code == 200:
    print("[OK] Workflow updated")

    # Check if it's still archived
    check_response = requests.get(f"{N8N_URL}/api/v1/workflows/{GMAIL_WF_ID}", headers=headers)
    if check_response.status_code == 200:
        updated_workflow = check_response.json()
        is_archived = updated_workflow.get('isArchived', False)
        print(f"New status: Archived={is_archived}")

        if is_archived:
            print("\n[INFO] The workflow is still archived.")
            print("The n8n API doesn't support programmatic unarchiving.")
            print("\nYOU MUST UNARCHIVE IT MANUALLY:")
            print("1. Go to: http://192.168.0.14:5678")
            print("2. Click on your profile/menu")
            print("3. Look for 'Archived Workflows' or similar")
            print("4. Find 'AIPA - Advanced Gmail Organization & Cleanup'")
            print("5. Click 'Unarchive' or 'Restore'")
        else:
            print("\n[SUCCESS] Workflow is now unarchived and visible!")
else:
    print(f"[FAIL] Update failed: {update_response.status_code}")
    print(f"Response: {update_response.text}")

print("\n" + "=" * 80)
print("ALTERNATIVE: CREATE A FRESH WORKFLOW")
print("=" * 80)
print("\nIf you prefer, I can create a brand new Gmail cleanup workflow")
print("instead of using the archived one. Would you like me to do that?")
print("\nWorkflow details:")
print(f"  Name: {workflow['name']}")
print(f"  Nodes: {len(workflow['nodes'])}")
print(f"  ID: {GMAIL_WF_ID}")
print("=" * 80)
