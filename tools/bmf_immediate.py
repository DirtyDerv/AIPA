#!/usr/bin/env python3
"""
IMMEDIATE BMF SOLUTION - Command Line Interface
Process your BMF work entry immediately via command line

NOTE: Replace webhook URLs and API keys with actual values from config/CREDENTIALS.md
"""

import requests
import json
from datetime import datetime
import webbrowser
import os

def process_bmf_immediate():
    """Process BMF work entry immediately"""
    
    print("🚀 IMMEDIATE BMF SOLUTION")
    print("=" * 25)
    
    # Discord webhook for confirmations (replace with actual webhook)
    discord_webhook = "YOUR_DISCORD_WEBHOOK_URL_HERE"
    
    # Supabase config (replace with actual credentials)
    supabase_url = "YOUR_SUPABASE_URL_HERE/rest/v1/conversations"
    supabase_headers = {
        'Content-Type': 'application/json',
        'apikey': 'YOUR_SUPABASE_ANON_KEY_HERE',
        'Authorization': 'Bearer YOUR_SUPABASE_ANON_KEY_HERE',
        'Prefer': 'return=minimal'
    }
    
    print("📝 Enter your BMF work entry:")
    print("(Example: tomorrow eddison and wanless fitting leadscrew)")
    
    # Get user input
    work_entry = input("\n🔨 BMF Work: ").strip()
    
    if not work_entry:
        print("❌ No work entry provided")
        return False
    
    print(f"\n⚡ Processing: {work_entry}")
    
    # Prepare data
    timestamp = datetime.now().isoformat()
    db_data = {
        'user_id': 'woody',
        'message': work_entry,
        'timestamp': timestamp,
        'message_type': 'work_log'
    }
    
    # Try to save to database
    db_success = False
    try:
        response = requests.post(supabase_url, json=db_data, headers=supabase_headers)
        db_success = response.status_code in [200, 201]
        if not db_success:
            print(f"⚠️ Database warning: {response.status_code}")
            print("Will still send to Discord...")
    except Exception as e:
        print(f"⚠️ Database error: {e}")
        print("Will still send to Discord...")
    
    # Send to Discord webhook
    discord_data = {
        "embeds": [{
            "title": "✅ BMF Work Entry",
            "description": work_entry,
            "color": 16753920,
            "fields": [
                {"name": "User", "value": "woody", "inline": True},
                {"name": "Time", "value": datetime.now().strftime("%H:%M"), "inline": True},
                {"name": "Database", "value": "✅ Saved" if db_success else "⚠️ Partial", "inline": True}
            ],
            "footer": {"text": "BMF Immediate Logger"}
        }]
    }
    
    discord_success = False
    try:
        discord_response = requests.post(discord_webhook, json=discord_data)
        discord_success = discord_response.status_code == 204
    except Exception as e:
        print(f"⚠️ Discord error: {e}")
    
    # Results
    print("\n" + "=" * 25)
    print("📋 RESULTS:")
    print(f"   Work Entry: {work_entry}")
    print(f"   Database: {'\u2705 Saved' if db_success else '\u26a0\ufe0f Failed'}")
    print(f"   Discord: {'\u2705 Sent' if discord_success else '\u26a0\ufe0f Failed'}")
    
    if discord_success or db_success:
        print("\n✅ BMF work entry logged successfully!")
        return True
    else:
        print("\n❌ Failed to log BMF work entry")
        return False

def show_alternatives():
    """Show alternative BMF logging methods"""
    print("\n🔧 OTHER BMF LOGGING OPTIONS:")
    print("\n1. 🤖 Discord Bot (if running):")
    print("   - Type in Discord: 'BMF work: your description'")
    print("   - Or use command: /bmf your description")
    
    print("\n2. 🌐 Web Interface:")
    print("   - Open: web/bmf_web_logger.html")
    print("   - Fill form and submit")
    
    print("\n3. 🔗 n8n Workflow:")
    print("   - Direct webhook: http://YOUR_N8N_SERVER_IP:5678/webhook/bmf-fixed")
    
if __name__ == "__main__":
    try:
        success = process_bmf_immediate()
        if not success:
            show_alternatives()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        show_alternatives()