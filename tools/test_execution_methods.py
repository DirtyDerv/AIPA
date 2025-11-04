#!/usr/bin/env python3
import requests
import json

N8N_URL = 'http://192.168.0.14:5678'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk'
WORKFLOW_ID = 'wnvzXLgk0W75yC4j'

headers = {
    'X-N8N-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}

print("🔍 Testing different execution endpoints...")

# Try method 1: POST execute
try:
    response = requests.post(f'{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}/execute', headers=headers)
    print(f"Method 1 - POST execute: {response.status_code}")
    if response.status_code != 404:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Method 1 error: {e}")

# Try method 2: GET workflow details first
try:
    response = requests.get(f'{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}', headers=headers)
    print(f"Method 2 - GET workflow: {response.status_code}")
    if response.status_code == 200:
        workflow = response.json()
        has_webhook = any('webhook' in str(node).lower() for node in workflow.get('nodes', []))
        has_trigger = any(node.get('type', '').endswith('.trigger') for node in workflow.get('nodes', []))
        print(f"Has webhook trigger: {has_webhook}")
        print(f"Has trigger nodes: {has_trigger}")
except Exception as e:
    print(f"Method 2 error: {e}")

# Try method 3: Check executions endpoint
try:
    response = requests.get(f'{N8N_URL}/api/v1/executions', headers=headers, params={'limit': 5})
    print(f"Method 3 - GET executions: {response.status_code}")
    if response.status_code == 200:
        executions = response.json()
        print(f"Recent executions found: {len(executions.get('data', []))}")
except Exception as e:
    print(f"Method 3 error: {e}")

print("✅ Analysis complete")