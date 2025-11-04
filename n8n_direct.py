#!/usr/bin/env python3
"""
Direct n8n API client using functions from MCP server
"""

import requests
import json
import os
from typing import Optional

class N8nAPIClient:
    def __init__(self):
        self.n8n_url = 'http://localhost:5678'
        self.api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk'

    def _get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['X-N8N-API-KEY'] = self.api_key
        return headers

    def _make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        url = f"{self.n8n_url}/api/v1{endpoint}"
        headers = self._get_headers()

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                return {'error': f'Unsupported method: {method}'}

            if response.status_code >= 200 and response.status_code < 300:
                return response.json() if response.content else {'success': True}
            else:
                return {
                    'error': f'HTTP {response.status_code}',
                    'message': response.text
                }

        except Exception as e:
            return {'error': str(e)}

    def list_workflows(self, active_only: bool = False):
        """List all workflows"""
        result = self._make_request('GET', '/workflows')
        if 'error' not in result:
            workflows = result.get('data', [])
            if active_only:
                workflows = [w for w in workflows if w.get('active')]
            return workflows
        return result

    def get_workflow(self, workflow_id: str):
        """Get workflow details"""
        return self._make_request('GET', f'/workflows/{workflow_id}')

    def create_workflow(self, name: str, workflow_json: str, activate: bool = False):
        """Create a new workflow"""
        data = {
            'name': name,
            'nodes': json.loads(workflow_json).get('nodes', []),
            'connections': json.loads(workflow_json).get('connections', {}),
            'active': activate,
            'settings': json.loads(workflow_json).get('settings', {}),
            'staticData': json.loads(workflow_json).get('staticData')
        }
        return self._make_request('POST', '/workflows', data)

    def update_workflow(self, workflow_id: str, workflow_json: str, activate: bool = False):
        """Update existing workflow"""
        data = {
            'nodes': json.loads(workflow_json).get('nodes', []),
            'connections': json.loads(workflow_json).get('connections', {}),
            'active': activate,
            'settings': json.loads(workflow_json).get('settings', {}),
            'staticData': json.loads(workflow_json).get('staticData')
        }
        return self._make_request('PUT', f'/workflows/{workflow_id}', data)

    def activate_workflow(self, workflow_id: str, active: bool = True):
        """Activate/deactivate workflow"""
        data = {'active': active}
        return self._make_request('PUT', f'/workflows/{workflow_id}', data)

    def delete_workflow(self, workflow_id: str):
        """Delete workflow"""
        return self._make_request('DELETE', f'/workflows/{workflow_id}')

    def test_webhook(self, webhook_path: str, test_data: dict = None):
        """Test webhook endpoint"""
        if test_data is None:
            test_data = {
                'content': 'test message',
                'author': {'username': 'test'},
                'channel_id': '123',
                'timestamp': '2024-01-01T00:00:00Z'
            }

        url = f"{self.n8n_url}/webhook/{webhook_path}"
        try:
            response = requests.post(url, json=test_data, timeout=10)
            return {
                'status_code': response.status_code,
                'response': response.text,
                'success': response.status_code == 200
            }
        except Exception as e:
            return {'error': str(e)}

# Global client instance
n8n_client = N8nAPIClient()

def list_n8n_workflows():
    """List all n8n workflows"""
    print("📋 Listing n8n workflows...")
    workflows = n8n_client.list_workflows()
    if 'error' in workflows:
        print(f"❌ Error: {workflows['error']}")
        return None

    print(f"Found {len(workflows)} workflows:")
    for wf in workflows:
        status = "🟢 ACTIVE" if wf.get('active') else "🔴 INACTIVE"
        print(f"  {wf.get('id')}: {wf.get('name')} {status}")
    return workflows

def activate_discord_nlp_workflow():
    """Find and activate the Discord NLP workflow"""
    print("🔍 Looking for Discord NLP workflow...")

    workflows = n8n_client.list_workflows()
    if 'error' in workflows:
        print(f"❌ Cannot list workflows: {workflows['error']}")
        return False

    # Look for Discord NLP workflow
    discord_wf = None
    for wf in workflows:
        if 'discord' in wf.get('name', '').lower() and 'nlp' in wf.get('name', '').lower():
            discord_wf = wf
            break

    if not discord_wf:
        print("❌ Discord NLP workflow not found. Creating it...")

        # Load workflow JSON
        try:
            with open('../n8n-workflows/09-discord-natural-language.json', 'r') as f:
                workflow_json = f.read()
        except FileNotFoundError:
            print("❌ Workflow file not found: ../n8n-workflows/09-discord-natural-language.json")
            return False

        # Create workflow
        result = n8n_client.create_workflow(
            name="Discord Natural Language Processing",
            workflow_json=workflow_json,
            activate=True
        )

        if 'error' in result:
            print(f"❌ Failed to create workflow: {result['error']}")
            return False
        else:
            print("✅ Workflow created and activated!")
            return True

    # Workflow exists, check if active
    if discord_wf.get('active'):
        print("✅ Discord NLP workflow is already active!")
        return True
    else:
        print("🔄 Activating Discord NLP workflow...")
        result = n8n_client.activate_workflow(discord_wf['id'], True)
        if 'error' in result:
            print(f"❌ Failed to activate: {result['error']}")
            return False
        else:
            print("✅ Workflow activated!")
            return True

def test_discord_webhook():
    """Test the Discord NLP webhook"""
    print("🧪 Testing Discord NLP webhook...")
    result = n8n_client.test_webhook('discord-nlp')

    if 'error' in result:
        print(f"❌ Webhook test failed: {result['error']}")
        return False

    if result.get('success'):
        print("✅ Webhook test successful!")
        return True
    else:
        print(f"❌ Webhook returned status {result.get('status_code')}: {result.get('response')}")
        return False

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'list':
            list_n8n_workflows()
        elif command == 'activate':
            activate_discord_nlp_workflow()
        elif command == 'test':
            test_discord_webhook()
        else:
            print("Usage: python n8n_direct.py [list|activate|test]")
    else:
        print("🔧 n8n Direct API Client")
        print("Usage: python n8n_direct.py [command]")
        print("Commands:")
        print("  list     - List all workflows")
        print("  activate - Find/create and activate Discord NLP workflow")
        print("  test     - Test Discord NLP webhook")