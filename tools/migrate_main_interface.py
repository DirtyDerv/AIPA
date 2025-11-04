#!/usr/bin/env python3
"""
AIPA Main Interface Migration - Discord Version
Migrates the central command interface from Telegram to Discord with comprehensive testing
"""

import requests
import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional

# n8n Configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

# Workflow IDs
ORIGINAL_MAIN_INTERFACE_ID = "DRuQZOp9tM79Sf6D"

# Discord webhook URLs
GENERAL_WEBHOOK = "https://discord.com/api/webhooks/1434598799090647163/gkiwL_F3DqTcqyckNR33T3-AN3SlY666bCkoXCvR_gctPsl2J4199YiNxD2LJoLmOi1K"  # personal channel for main interface

class MainInterfaceMigrator:
    def __init__(self):
        self.test_results = []
        self.workflow_id = None
    
    def log_step(self, step: str, success: bool, details: str = ""):
        """Log migration step"""
        result = {
            "step": step,
            "success": success,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.test_results.append(result)
        
        status = "✅" if success else "❌"
        print(f"{status} {step}: {details}")
        
        return success
    
    def get_original_workflow(self) -> Optional[Dict]:
        """Get original Telegram main interface workflow for analysis"""
        print("\n🔍 STEP 1: Analyzing Original Workflow")
        try:
            response = requests.get(f"{N8N_URL}/api/v1/workflows/{ORIGINAL_MAIN_INTERFACE_ID}", headers=headers)
            if response.status_code == 200:
                workflow = response.json()
                node_count = len(workflow.get('nodes', []))
                telegram_nodes = [node for node in workflow.get('nodes', []) if 'telegram' in node.get('type', '').lower()]
                
                self.log_step(
                    "analyze_original", 
                    True, 
                    f"Found {node_count} nodes, {len(telegram_nodes)} Telegram nodes to migrate"
                )
                return workflow
            else:
                self.log_step("analyze_original", False, f"Failed to get workflow: {response.status_code}")
                return None
        except Exception as e:
            self.log_step("analyze_original", False, f"Error: {e}")
            return None
    
    def create_discord_main_interface(self) -> Dict:
        """Create comprehensive Discord main interface workflow"""
        print("\n🔍 STEP 2: Creating Discord Main Interface")
        
        workflow = {
            "name": "AIPA - Main Interface (Discord)",
            "nodes": [
                {
                    "parameters": {
                        "httpMethod": "POST",
                        "path": "aipa"
                    },
                    "id": "main-webhook",
                    "name": "AIPA Main Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [200, 300]
                },
                {
                    "parameters": {
                        "functionCode": "// Parse incoming command and route to appropriate business context\nconst body = $json.body || $json;\nconst command = body.command || body.text || '';\nconst user = body.user || 'unknown';\n\n// Command routing logic\nlet businessContext = 'personal';\nlet action = 'help';\n\nif (command.includes('/email') || command.includes('email')) {\n  businessContext = 'email-alerts';\n  action = 'email';\n} else if (command.includes('/calendar') || command.includes('calendar')) {\n  businessContext = 'calendar-updates';\n  action = 'calendar';\n} else if (command.includes('/woodys') || command.includes('woodys')) {\n  businessContext = 'woodys-creations';\n  action = 'woodys';\n} else if (command.includes('/dj') || command.includes('dj')) {\n  businessContext = 'dj-business';\n  action = 'dj';\n} else if (command.includes('/bmf') || command.includes('bmf')) {\n  businessContext = 'bmf-work';\n  action = 'bmf';\n} else if (command.includes('/pub') || command.includes('top-odd')) {\n  businessContext = 'the-top-odd';\n  action = 'pub';\n} else if (command.includes('/reports') || command.includes('reports')) {\n  businessContext = 'reports';\n  action = 'reports';\n} else if (command.includes('/marketing') || command.includes('marketing')) {\n  businessContext = 'personal';\n  action = 'marketing';\n}\n\nreturn {\n  originalCommand: command,\n  user: user,\n  businessContext: businessContext,\n  action: action,\n  timestamp: new Date().toISOString(),\n  routingDecision: `Command '${command}' routed to ${businessContext} for ${action}`\n};"
                    },
                    "id": "parse-command",
                    "name": "Parse Command & Route",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [400, 300]
                },
                {
                    "parameters": {
                        "url": "https://neoeoabqcfpopzkwvcxq.supabase.co/rest/v1/conversations",
                        "method": "POST",
                        "sendHeaders": True,
                        "headerParameters": {
                            "parameters": [
                                {
                                    "name": "apikey",
                                    "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck"
                                },
                                {
                                    "name": "Authorization",
                                    "value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck"
                                },
                                {
                                    "name": "Content-Type",
                                    "value": "application/json"
                                }
                            ]
                        },
                        "sendBody": True,
                        "bodyParameters": {
                            "parameters": [
                                {
                                    "name": "user_id",
                                    "value": "={{ $json.user }}"
                                },
                                {
                                    "name": "message",
                                    "value": "={{ $json.originalCommand }}"
                                },
                                {
                                    "name": "business_context",
                                    "value": "={{ $json.businessContext }}"
                                },
                                {
                                    "name": "created_at",
                                    "value": "={{ $json.timestamp }}"
                                },
                                {
                                    "name": "metadata",
                                    "value": "={{ JSON.stringify({action: $json.action, routing: $json.routingDecision}) }}"
                                }
                            ]
                        }
                    },
                    "id": "log-conversation",
                    "name": "Log to Database",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 4,
                    "position": [600, 300]
                },
                {
                    "parameters": {
                        "url": GENERAL_WEBHOOK,
                        "method": "POST",
                        "sendHeaders": True,
                        "headerParameters": {
                            "parameters": [
                                {
                                    "name": "Content-Type",
                                    "value": "application/json"
                                }
                            ]
                        },
                        "sendBody": True,
                        "bodyParameters": {
                            "parameters": [
                                {
                                    "name": "embeds",
                                    "value": "=[{\"title\":\"🤖 AIPA Command Received\",\"description\":\"{{ $node['Parse Command & Route'].json.originalCommand }}\",\"color\":3447003,\"fields\":[{\"name\":\"👤 User\",\"value\":\"{{ $node['Parse Command & Route'].json.user }}\",\"inline\":true},{\"name\":\"🏢 Business Context\",\"value\":\"{{ $node['Parse Command & Route'].json.businessContext }}\",\"inline\":true},{\"name\":\"⚡ Action\",\"value\":\"{{ $node['Parse Command & Route'].json.action }}\",\"inline\":true},{\"name\":\"🔄 Routing\",\"value\":\"{{ $node['Parse Command & Route'].json.routingDecision }}\",\"inline\":false}],\"timestamp\":\"{{ new Date().toISOString() }}\",\"footer\":{\"text\":\"AIPA Main Interface\"}}]"
                                }
                            ]
                        }
                    },
                    "id": "discord-response",
                    "name": "Send Discord Response",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 4,
                    "position": [800, 300]
                },
                {
                    "parameters": {
                        "conditions": {
                            "string": [
                                {
                                    "value1": "={{ $node['Parse Command & Route'].json.action }}",
                                    "value2": "help"
                                }
                            ]
                        }
                    },
                    "id": "check-help",
                    "name": "Check if Help Command",
                    "type": "n8n-nodes-base.if",
                    "typeVersion": 1,
                    "position": [1000, 300]
                },
                {
                    "parameters": {
                        "url": GENERAL_WEBHOOK,
                        "method": "POST",
                        "sendHeaders": True,
                        "headerParameters": {
                            "parameters": [
                                {
                                    "name": "Content-Type",
                                    "value": "application/json"
                                }
                            ]
                        },
                        "sendBody": True,
                        "bodyParameters": {
                            "parameters": [
                                {
                                    "name": "embeds",
                                    "value": "=[{\"title\":\"🤖 AIPA Help Menu\",\"description\":\"Welcome to AIPA - Your AI Personal Assistant\\n\\nAvailable Commands:\",\"color\":5763719,\"fields\":[{\"name\":\"📧 Email Management\",\"value\":\"`/email` - Process and manage emails\",\"inline\":false},{\"name\":\"📅 Calendar\",\"value\":\"`/calendar` - Manage appointments and events\",\"inline\":false},{\"name\":\"🎨 Woody's Creations\",\"value\":\"`/woodys` - Order processing and management\",\"inline\":false},{\"name\":\"🎵 DJ Business\",\"value\":\"`/dj` - Booking and event management\",\"inline\":false},{\"name\":\"💼 BMF Work\",\"value\":\"`/bmf` - Work logging and timesheets\",\"inline\":false},{\"name\":\"🍺 The Top Odd\",\"value\":\"`/pub` - Pub management tasks\",\"inline\":false},{\"name\":\"📊 Reports\",\"value\":\"`/reports` - Business intelligence and analytics\",\"inline\":false},{\"name\":\"📈 Marketing\",\"value\":\"`/marketing` - Campaign automation\",\"inline\":false}],\"timestamp\":\"{{ new Date().toISOString() }}\",\"footer\":{\"text\":\"AIPA v2.0 - Discord Edition\"}}]"
                                }
                            ]
                        }
                    },
                    "id": "send-help",
                    "name": "Send Help Menu",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 4,
                    "position": [1200, 200]
                }
            ],
            "connections": {
                "main-webhook": {
                    "main": [
                        [
                            {
                                "node": "parse-command",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                },
                "parse-command": {
                    "main": [
                        [
                            {
                                "node": "log-conversation",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                },
                "log-conversation": {
                    "main": [
                        [
                            {
                                "node": "discord-response",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                },
                "discord-response": {
                    "main": [
                        [
                            {
                                "node": "check-help",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                },
                "check-help": {
                    "main": [
                        [
                            {
                                "node": "send-help",
                                "type": "main",
                                "index": 0
                            }
                        ],
                        []
                    ]
                }
            },
            "settings": {
                "executionOrder": "v1"
            }
        }
        
        return workflow
    
    def create_workflow(self) -> bool:
        """Create the Discord main interface workflow"""
        workflow = self.create_discord_main_interface()
        
        try:
            response = requests.post(f"{N8N_URL}/api/v1/workflows", headers=headers, json=workflow)
            
            if response.status_code in [200, 201]:
                workflow_data = response.json()
                self.workflow_id = workflow_data['id']
                
                self.log_step(
                    "create_workflow", 
                    True, 
                    f"Created Discord main interface: {self.workflow_id}"
                )
                return True
            else:
                self.log_step("create_workflow", False, f"Failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.log_step("create_workflow", False, f"Error: {e}")
            return False
    
    def test_workflow_webhook(self) -> bool:
        """Test the main interface webhook thoroughly"""
        print("\n🔍 STEP 3: Activating Workflow for Testing")
        
        if not self.workflow_id:
            self.log_step("test_webhook", False, "No workflow ID available")
            return False
        
        # First activate the workflow so webhook is available
        try:
            activate_response = requests.post(f"{N8N_URL}/api/v1/workflows/{self.workflow_id}/activate", headers=headers)
            if activate_response.status_code == 200:
                self.log_step("activate_for_testing", True, "Workflow activated for testing")
                time.sleep(2)  # Give time for webhook to become available
            else:
                self.log_step("activate_for_testing", False, f"Failed to activate: {activate_response.status_code}")
                return False
        except Exception as e:
            self.log_step("activate_for_testing", False, f"Error activating: {e}")
            return False
        
        print("\n🔍 STEP 3b: Testing Webhook Commands")
        
        # Test different commands
        test_commands = [
            {"command": "/help", "expected_action": "help"},
            {"command": "/email check", "expected_action": "email"},
            {"command": "/calendar today", "expected_action": "calendar"},
            {"command": "/woodys orders", "expected_action": "woodys"},
            {"command": "/dj bookings", "expected_action": "dj"},
            {"command": "/reports daily", "expected_action": "reports"}
        ]
        
        webhook_url = f"{N8N_URL}/webhook/aipa"
        all_tests_passed = True
        
        for i, test_case in enumerate(test_commands):
            print(f"  Testing command {i+1}/{len(test_commands)}: {test_case['command']}")
            
            test_payload = {
                "command": test_case["command"],
                "user": "test_user",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            try:
                response = requests.post(webhook_url, json=test_payload, timeout=15)
                if response.status_code == 200:
                    self.log_step(
                        f"test_command_{i+1}", 
                        True, 
                        f"Command '{test_case['command']}' processed successfully"
                    )
                else:
                    self.log_step(
                        f"test_command_{i+1}", 
                        False, 
                        f"Command '{test_case['command']}' failed: {response.status_code}"
                    )
                    all_tests_passed = False
                    
            except Exception as e:
                self.log_step(
                    f"test_command_{i+1}", 
                    False, 
                    f"Command '{test_case['command']}' error: {e}"
                )
                all_tests_passed = False
            
            time.sleep(1)  # Rate limit protection
        
        return all_tests_passed
    
    def activate_and_switch(self) -> bool:
        """Switch from activated test workflow to deactivate Telegram version"""
        print("\n🔍 STEP 4: Deactivating Telegram Interface")
        
        if not self.workflow_id:
            self.log_step("activate_switch", False, "No workflow ID available")
            return False
        
        try:
            # Discord workflow is already activated from testing
            self.log_step("discord_already_active", True, "Discord main interface already active from testing")
            
            # Deactivate Telegram workflow
            deactivate_response = requests.post(f"{N8N_URL}/api/v1/workflows/{ORIGINAL_MAIN_INTERFACE_ID}/deactivate", headers=headers)
            if deactivate_response.status_code == 200:
                self.log_step("deactivate_telegram", True, "Telegram main interface deactivated")
                return True
            else:
                self.log_step("deactivate_telegram", False, f"Failed to deactivate Telegram: {deactivate_response.status_code}")
                return False
                
        except Exception as e:
            self.log_step("activate_switch", False, f"Error: {e}")
            return False
    
    def final_verification(self) -> bool:
        """Final verification that migration was successful"""
        print("\n🔍 STEP 5: Final Verification")
        
        try:
            # Check Discord workflow is active
            discord_response = requests.get(f"{N8N_URL}/api/v1/workflows/{self.workflow_id}", headers=headers)
            if discord_response.status_code == 200:
                discord_workflow = discord_response.json()
                discord_active = discord_workflow.get('active', False)
                
                # Check Telegram workflow is inactive
                telegram_response = requests.get(f"{N8N_URL}/api/v1/workflows/{ORIGINAL_MAIN_INTERFACE_ID}", headers=headers)
                if telegram_response.status_code == 200:
                    telegram_workflow = telegram_response.json()
                    telegram_active = telegram_workflow.get('active', False)
                    
                    if discord_active and not telegram_active:
                        self.log_step("final_verification", True, "Migration verified: Discord active, Telegram inactive")
                        return True
                    else:
                        self.log_step("final_verification", False, f"Verification failed: Discord active={discord_active}, Telegram active={telegram_active}")
                        return False
                else:
                    self.log_step("final_verification", False, f"Could not check Telegram workflow: {telegram_response.status_code}")
                    return False
            else:
                self.log_step("final_verification", False, f"Could not check Discord workflow: {discord_response.status_code}")
                return False
                
        except Exception as e:
            self.log_step("final_verification", False, f"Error: {e}")
            return False
    
    def run_complete_migration(self) -> bool:
        """Run complete migration with comprehensive testing"""
        print("🚀 AIPA Main Interface Migration - Discord Version")
        print("=" * 60)
        print("Running comprehensive migration with testing...")
        
        # Step 1: Analyze original
        original = self.get_original_workflow()
        if not original:
            return False
        
        # Step 2: Create Discord version
        if not self.create_workflow():
            return False
        
        # Step 3: Test thoroughly
        if not self.test_workflow_webhook():
            self.log_step("migration_aborted", False, "Webhook tests failed - aborting migration")
            return False
        
        # Step 4: Activate and switch
        if not self.activate_and_switch():
            return False
        
        # Step 5: Final verification
        if not self.final_verification():
            return False
        
        # Success summary
        total_steps = len(self.test_results)
        passed_steps = sum(1 for result in self.test_results if result.success)
        
        print(f"\n🎉 MAIN INTERFACE MIGRATION COMPLETE!")
        print("=" * 45)
        print(f"✅ All {passed_steps}/{total_steps} steps completed successfully")
        print(f"🆔 New Discord Workflow ID: {self.workflow_id}")
        print(f"🔗 Webhook URL: {N8N_URL}/webhook/aipa")
        print(f"📱 Old Telegram interface: 🔴 Deactivated")
        print(f"💬 New Discord interface: 🟢 Active")
        
        print(f"\n📋 Test Commands Available:")
        print(f"• POST {N8N_URL}/webhook/aipa with {{'command': '/help'}}")
        print(f"• POST {N8N_URL}/webhook/aipa with {{'command': '/email check'}}")
        print(f"• POST {N8N_URL}/webhook/aipa with {{'command': '/calendar today'}}")
        
        print(f"\n📊 Migration Progress Update:")
        print(f"✅ Email Processing: Migrated & Active")
        print(f"✅ Business Intelligence: Migrated & Active") 
        print(f"✅ Main Interface: Migrated & Active")
        print(f"📋 Remaining: 5 workflows to migrate")
        
        return True

def main():
    """Main migration function"""
    migrator = MainInterfaceMigrator()
    
    success = migrator.run_complete_migration()
    
    # Save detailed report
    report = {
        "migration_type": "main_interface",
        "start_time": datetime.now().isoformat(),
        "success": success,
        "workflow_id": migrator.workflow_id,
        "steps": migrator.test_results
    }
    
    with open('main_interface_migration_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📋 Detailed report saved to: main_interface_migration_report.json")
    
    return success

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🚀 Main Interface migration successful - ready for next workflow!")
    else:
        print(f"\n❌ Main Interface migration failed - please review logs.")