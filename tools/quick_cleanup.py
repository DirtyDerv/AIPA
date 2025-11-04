#!/usr/bin/env python3
"""
Quick cleanup script
"""

import os
import shutil
from datetime import datetime

def cleanup_now():
    # Create backup
    backup_dir = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    os.makedirs(backup_dir, exist_ok=True)

    files_to_delete = [
        'activate_all_workflows.py', 'activate_bi_workflow.py', 'activate_bmf_final.py',
        'activate_bmf_now.py', 'activate_email_workflow.py', 'activate_remaining_workflows.py',
        'activate_simple.py', 'activate_workflows_fixed.py', 'activate_workflows.py',
        'bulk_migrate_remaining.py', 'check_active_workflows.py', 'check_bmf_error_detail.py',
        'check_bmf_parse_issue.py', 'check_bmf_workflow.py', 'check_execution_errors.py',
        'check_gmail_workflows.py', 'check_main_interface.py', 'check_webhook_config.py',
        'check_webhook_conflicts.py', 'check_workflow_credentials.py', 'check_workflow_issues.py',
        'check_workflows_debug.py', 'comprehensive_migration_tester.py', 'debug_workflow.py',
        'diagnose_bmf_flow.py', 'diagnose_bmf_routing.py', 'diagnose_discord_bmf.py',
        'create_conversations_table.sql', 'create_discord_bi_workflow.py', 'create_gmail_organizer.py',
        'create_minimal_bmf.py', 'create_new_bmf_workflow.py', 'create_simple_discord_email.py',
        'create_working_bmf.py', 'fix_and_upload_calendar.py', 'fix_bmf_parse_safely.py',
        'fix_bmf_properly.py', 'fix_bmf_webhook.py', 'fix_bmf_workflow.py',
        'fix_discord_bmf_now.py', 'fix_discord_bot_replies.py', 'final_bmf_integration.py',
        'final_main_interface_fix.py', 'final_migration_report.py', 'AIPA_MIGRATION_FINAL_REPORT.json',
        'API_UPDATE_SUMMARY.md', 'bulk_migration_report.json', 'calendar_migration_report.json',
        'discord_voice_setup_report.json', 'test_bmf_workflow.py', 'test_bot_permissions.py',
        'discord_deployment_analysis.py', 'analyze_cleanup.py', 'cleanup_project.py'
    ]

    backed_up = 0
    deleted = 0

    for file in files_to_delete:
        if os.path.exists(file):
            try:
                shutil.copy2(file, backup_dir)
                backed_up += 1
                os.remove(file)
                deleted += 1
                print(f'🗑️ Deleted: {file}')
            except Exception as e:
                print(f'❌ Error with {file}: {e}')

    print(f'\n✅ CLEANUP COMPLETE!')
    print(f'📦 Backup: {backup_dir} ({backed_up} files)')
    print(f'🗑️ Deleted: {deleted} files')

if __name__ == "__main__":
    cleanup_now()