#!/usr/bin/env python3
"""
Test Gmail Connection Script
Tests if Gmail API credentials are working in n8n
"""

import requests
import json
import sys
from datetime import datetime

# n8n configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def test_gmail_workflow():
    """Test the Gmail organization workflow"""
    print("🔍 Testing Gmail Organization Workflow...")
    
    try:
        # Get the workflow details
        workflow_id = "wnvzXLgk0W75yC4j"
        response = requests.get(f"{N8N_URL}/api/v1/workflows/{workflow_id}", headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Failed to get workflow: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        workflow = response.json()
        print(f"✅ Workflow found: {workflow['name']}")
        print(f"   Active: {workflow['active']}")
        print(f"   Nodes: {len(workflow['nodes'])}")
        
        # Check for Gmail nodes
        gmail_nodes = [node for node in workflow['nodes'] if 'gmail' in node.get('type', '').lower()]
        print(f"   Gmail nodes: {len(gmail_nodes)}")
        
        # Check credentials
        credentials_used = set()
        for node in workflow['nodes']:
            if 'credentials' in node:
                for cred_type, cred_id in node['credentials'].items():
                    credentials_used.add(f"{cred_type}: {cred_id}")
        
        print(f"   Credentials used: {len(credentials_used)}")
        for cred in credentials_used:
            print(f"     - {cred}")
        
        # Get recent executions
        exec_response = requests.get(f"{N8N_URL}/api/v1/executions?workflowId={workflow_id}&limit=5", headers=headers)
        if exec_response.status_code == 200:
            executions = exec_response.json()
            print(f"   Recent executions: {len(executions['data'])}")
            for exec in executions['data'][:3]:
                print(f"     - {exec['startedAt']}: {exec['status']}")
        
        # Check if it's scheduled
        cron_nodes = [node for node in workflow['nodes'] if node.get('type') == 'n8n-nodes-base.cron']
        if cron_nodes:
            cron_node = cron_nodes[0]
            rule = cron_node.get('parameters', {}).get('rule', 'Unknown')
            print(f"   Schedule: {rule}")
        else:
            print("   ⚠️  No cron trigger found!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing workflow: {e}")
        return False

def test_credentials():
    """Test if Gmail credentials are available"""
    print("\n🔑 Testing Gmail Credentials...")
    
    try:
        response = requests.get(f"{N8N_URL}/api/v1/credentials", headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Failed to get credentials: {response.status_code}")
            return False
            
        credentials = response.json()
        gmail_creds = [cred for cred in credentials['data'] if 'gmail' in cred.get('type', '').lower()]
        
        print(f"✅ Total credentials: {len(credentials['data'])}")
        print(f"   Gmail credentials: {len(gmail_creds)}")
        
        for cred in gmail_creds:
            print(f"     - {cred['name']} (ID: {cred['id']}, Type: {cred['type']})")
        
        return len(gmail_creds) > 0
        
    except Exception as e:
        print(f"❌ Error testing credentials: {e}")
        return False

def manual_trigger_test():
    """Try to manually trigger the Gmail workflow"""
    print("\n🚀 Testing Manual Trigger...")
    
    try:
        workflow_id = "wnvzXLgk0W75yC4j"
        
        # Try to trigger the workflow manually
        trigger_data = {
            "workflowId": workflow_id
        }
        
        response = requests.post(f"{N8N_URL}/api/v1/workflows/{workflow_id}/execute", 
                               headers=headers, json=trigger_data)
        
        if response.status_code == 201:
            execution = response.json()
            print(f"✅ Manual trigger successful!")
            print(f"   Execution ID: {execution['id']}")
            print(f"   Status: {execution['status']}")
            return True
        else:
            print(f"❌ Manual trigger failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error with manual trigger: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 GMAIL CONNECTION TEST")
    print("=" * 60)
    
    # Test workflow
    workflow_ok = test_gmail_workflow()
    
    # Test credentials
    creds_ok = test_credentials()
    
    # Test manual trigger
    trigger_ok = manual_trigger_test()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Workflow Status: {'✅ OK' if workflow_ok else '❌ Failed'}")
    print(f"Credentials:     {'✅ OK' if creds_ok else '❌ Failed'}")
    print(f"Manual Trigger:  {'✅ OK' if trigger_ok else '❌ Failed'}")
    
    if workflow_ok and creds_ok:
        print("\n💡 DIAGNOSIS:")
        print("   The Gmail workflow appears to be configured correctly.")
        print("   If it's not organizing emails, check:")
        print("   1. Gmail API quotas/limits")
        print("   2. OAuth token expiration")
        print("   3. Workflow schedule (should run daily)")
        print("   4. Email volume (might not have emails to organize)")
    else:
        print("\n🔧 FIXES NEEDED:")
        if not workflow_ok:
            print("   - Fix workflow configuration")
        if not creds_ok:
            print("   - Add/fix Gmail credentials in n8n")

if __name__ == "__main__":
    main()