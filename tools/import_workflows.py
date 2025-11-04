#!/usr/bin/env python3
"""
Import n8n workflows via REST API
"""

import requests
import json
import os
from pathlib import Path

# n8n Configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def list_workflows():
    """List all existing workflows"""
    response = requests.get(f"{N8N_URL}/api/v1/workflows", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        print(f"Error listing workflows: {response.status_code}")
        print(response.text)
        return []

def import_workflow(workflow_file):
    """Import a single workflow file"""
    print(f"\n{'='*60}")
    print(f"Importing: {workflow_file.name}")
    print(f"{'='*60}")

    try:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)

        # n8n API expects the workflow data directly
        # Remove any fields that might cause issues (tags is read-only)
        workflow_payload = {
            "name": workflow_data.get("name"),
            "nodes": workflow_data.get("nodes"),
            "connections": workflow_data.get("connections"),
            "settings": workflow_data.get("settings", {}),
            "staticData": workflow_data.get("staticData")
        }

        # POST to create workflow
        response = requests.post(
            f"{N8N_URL}/api/v1/workflows",
            headers=headers,
            json=workflow_payload
        )

        if response.status_code in [200, 201]:
            result = response.json()
            workflow_id = result.get('id')
            workflow_name = result.get('name')
            print(f"SUCCESS: Workflow imported")
            print(f"   ID: {workflow_id}")
            print(f"   Name: {workflow_name}")
            return True, workflow_id
        else:
            print(f"FAILED: {response.status_code}")
            print(f"   Error: {response.text}")
            return False, None

    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        return False, None

def activate_workflow(workflow_id):
    """Activate a workflow"""
    try:
        response = requests.patch(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            headers=headers,
            json={"active": True}
        )

        if response.status_code == 200:
            print(f"   Activated")
            return True
        else:
            print(f"   Could not activate: {response.status_code}")
            return False
    except Exception as e:
        print(f"   Activation error: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("n8n Workflow Importer - AIPA Project")
    print("="*60)

    # Check connection
    print("\nTesting connection to n8n...")
    existing = list_workflows()
    print(f"Connected! Current workflows: {len(existing)}")

    if existing:
        print("\nExisting workflows:")
        for wf in existing:
            print(f"   - {wf.get('name')} (ID: {wf.get('id')})")

    # Find workflow files
    workflows_dir = Path(__file__).parent.parent / "n8n-workflows"
    workflow_files = sorted(workflows_dir.glob("*.json"))

    if not workflow_files:
        print("\nNo workflow files found in n8n-workflows/")
        return

    print(f"\nFound {len(workflow_files)} workflow files to import")

    # Import each workflow
    imported = []
    failed = []

    for workflow_file in workflow_files:
        success, workflow_id = import_workflow(workflow_file)

        if success:
            imported.append((workflow_file.name, workflow_id))
            # Try to activate it
            if workflow_id:
                activate_workflow(workflow_id)
        else:
            failed.append(workflow_file.name)

    # Summary
    print("\n" + "="*60)
    print("IMPORT SUMMARY")
    print("="*60)
    print(f"Successfully imported: {len(imported)}")
    print(f"Failed: {len(failed)}")

    if imported:
        print("\nImported workflows:")
        for name, wf_id in imported:
            print(f"   - {name} (ID: {wf_id})")

    if failed:
        print("\nFailed workflows:")
        for name in failed:
            print(f"   - {name}")

    # Final status
    print("\n" + "="*60)
    final_count = list_workflows()
    print(f"Total workflows on server: {len(final_count)}")
    print("="*60)

    print("\nImport complete!")
    print("\nNext steps:")
    print("   1. Open n8n at http://192.168.0.14:5678")
    print("   2. Configure credentials (Telegram, Gmail, Supabase, Claude)")
    print("   3. Test the Telegram interface workflow")
    print("   4. Activate workflows you want to use")

if __name__ == "__main__":
    main()
