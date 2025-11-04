#!/usr/bin/env python3
"""
Gmail Organizer Test & Manual Execution Script
Run this to test your Gmail organizer workflow before automatic execution
"""

import requests
import json
import time
from datetime import datetime, timezone

# Configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"
WORKFLOW_ID = "wnvzXLgk0W75yC4j"  # Most recent Gmail Organizer Workflow ID

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

class GmailOrganizerTester:
    def __init__(self):
        self.execution_id = None
        
    def check_workflow_status(self):
        """Check if the Gmail organizer workflow is active"""
        print("🔍 Checking Gmail Organizer Workflow Status")
        
        try:
            response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers)
            
            if response.status_code == 200:
                workflow = response.json()
                is_active = workflow.get('active', False)
                name = workflow.get('name', 'Unknown')
                
                print(f"✅ Workflow Found: {name}")
                print(f"📊 Status: {'🟢 Active' if is_active else '🔴 Inactive'}")
                print(f"🆔 ID: {WORKFLOW_ID}")
                
                return is_active
            else:
                print(f"❌ Failed to get workflow: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error checking workflow: {e}")
            return False
    
    def run_manual_test(self):
        """Manually execute the Gmail organizer workflow"""
        print("\n🚀 Running Manual Gmail Organization Test")
        
        try:
            # Execute workflow manually
            response = requests.post(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}/execute", headers=headers)
            
            if response.status_code == 200:
                execution_data = response.json()
                self.execution_id = execution_data.get('data', {}).get('executionId')
                
                print(f"✅ Test execution started")
                print(f"🆔 Execution ID: {self.execution_id}")
                print("⏳ Processing... (this may take a few minutes)")
                
                return True
            else:
                print(f"❌ Failed to start execution: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting execution: {e}")
            return False
    
    def check_execution_status(self):
        """Check the status of the manual execution"""
        if not self.execution_id:
            print("❌ No execution ID available")
            return False
        
        print(f"\n📊 Checking execution status...")
        
        try:
            response = requests.get(f"{N8N_URL}/api/v1/executions/{self.execution_id}", headers=headers)
            
            if response.status_code == 200:
                execution = response.json()
                status = execution.get('status', 'unknown')
                finished = execution.get('finished', False)
                
                print(f"📈 Status: {status}")
                print(f"✅ Finished: {finished}")
                
                if finished:
                    if status == 'success':
                        print("🎉 Gmail organization completed successfully!")
                        self.display_execution_results(execution)
                    else:
                        print(f"⚠️ Execution finished with status: {status}")
                        self.display_execution_errors(execution)
                
                return finished
            else:
                print(f"❌ Failed to get execution status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error checking execution: {e}")
            return False
    
    def display_execution_results(self, execution):
        """Display results from successful execution"""
        print("\n📊 EXECUTION RESULTS")
        print("=" * 40)
        
        try:
            data = execution.get('data', {})
            result_data = data.get('resultData', {})
            
            # Look for our classification results
            for node_name, node_data in result_data.items():
                if 'classification' in node_name.lower():
                    for run in node_data:
                        if 'data' in run and 'main' in run['data']:
                            for item in run['data']['main']:
                                result = item.get('json', {})
                                
                                if 'summary' in result:
                                    summary = result['summary']
                                    print(f"📧 Emails Processed: {summary.get('total_processed', 0)}")
                                    print(f"🔒 Protected: {summary.get('protected_count', 0)}")
                                    print(f"🗑️ Marked for Cleanup: {summary.get('deletion_count', 0)}")
                                
                                if 'protected_emails' in result:
                                    protected = result['protected_emails']
                                    if protected:
                                        print(f"\n🛡️ PROTECTED EMAILS:")
                                        for email in protected[:5]:  # Show first 5
                                            print(f"   • {email.get('category', 'unknown')}: {email.get('subject', 'No subject')[:50]}...")
                                        
                                        if len(protected) > 5:
                                            print(f"   ... and {len(protected) - 5} more")
            
            print(f"\n✅ Check your Discord #email-alerts channel for the detailed report!")
            
        except Exception as e:
            print(f"Error displaying results: {e}")
    
    def display_execution_errors(self, execution):
        """Display errors from failed execution"""
        print("\n❌ EXECUTION ERRORS")
        print("=" * 40)
        
        try:
            data = execution.get('data', {})
            result_data = data.get('resultData', {})
            
            for node_name, node_data in result_data.items():
                for run in node_data:
                    if 'error' in run:
                        error = run['error']
                        print(f"🔴 {node_name}: {error.get('message', 'Unknown error')}")
            
        except Exception as e:
            print(f"Error displaying errors: {e}")
    
    def wait_for_completion(self, max_wait_minutes=10):
        """Wait for execution to complete"""
        print(f"\n⏳ Waiting for completion (max {max_wait_minutes} minutes)...")
        
        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60
        
        while time.time() - start_time < max_wait_seconds:
            if self.check_execution_status():
                return True
            
            print("⏳ Still processing...")
            time.sleep(30)  # Check every 30 seconds
        
        print(f"⚠️ Timeout after {max_wait_minutes} minutes")
        return False
    
    def run_full_test(self):
        """Run complete test sequence"""
        print("🧪 AIPA Gmail Organizer Test Suite")
        print("=" * 50)
        
        # Step 1: Check workflow status
        if not self.check_workflow_status():
            print("\n❌ Workflow is not active or not found")
            print("💡 Please check the workflow in n8n and ensure it's activated")
            return False
        
        # Step 2: Run manual test
        if not self.run_manual_test():
            print("\n❌ Failed to start manual test")
            return False
        
        # Step 3: Wait for completion
        success = self.wait_for_completion()
        
        if success:
            print("\n🎉 TEST COMPLETED SUCCESSFULLY!")
            print("=" * 40)
            print("✅ Your Gmail organizer is working properly")
            print("🔄 It will run automatically every day at 2:00 AM")
            print("📱 Check Discord #email-alerts for notifications")
            print("📊 Check Supabase for detailed logs")
        else:
            print("\n⚠️ TEST INCOMPLETE")
            print("💡 Check n8n execution logs for details")
        
        return success

def main():
    """Main test function"""
    tester = GmailOrganizerTester()
    
    print("🔧 Gmail Organizer Manual Test")
    print("This will test your Gmail organization workflow")
    print("Make sure you have:")
    print("  ✅ Gmail API credentials set up in n8n")
    print("  ✅ Discord webhooks configured") 
    print("  ✅ Supabase connection working")
    
    input("\nPress Enter to continue with the test...")
    
    success = tester.run_full_test()
    
    if success:
        print(f"\n🎊 Your Gmail will be automatically organized every night!")
        print(f"🛡️ Important emails will be protected and labeled")
        print(f"🗑️ Spam and old emails will be safely removed")
    else:
        print(f"\n🔧 Please check the setup and try again")
    
    return success

if __name__ == "__main__":
    main()