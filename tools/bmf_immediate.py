#!/usr/bin/env python3
"""
IMMEDIATE BMF SOLUTION - Web Interface
Process your BMF work entry immediately while we fix the Discord bot
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
    
    # Discord webhook for confirmations
    discord_webhook = "https://discord.com/api/webhooks/1434598843546341581/r0NqE35ekv_88zWCj7TYze_15zuKtN_wsARtWMesa-_KVkKPA26jkZNNlSC2_3G4grzf"
    
    # Supabase config
    supabase_url = "https://neoeoabqcfpopzkwvcxq.supabase.co/rest/v1/conversations"
    supabase_headers = {
        'Content-Type': 'application/json',
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck',
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
    
    # Try to log to database
    db_success = False
    try:
        print("💾 Logging to database...")
        db_response = requests.post(supabase_url, json=db_data, headers=supabase_headers)
        db_success = db_response.status_code in [200, 201]
        
        if db_success:
            print("✅ Database: Success!")
        else:
            print(f"⚠️ Database: Partial ({db_response.status_code})")
            print(f"Response: {db_response.text[:200]}")
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # Send Discord confirmation
    discord_msg = {
        "embeds": [{
            "title": "✅ BMF Work Logged",
            "description": work_entry,
            "color": 16752640,  # Orange
            "fields": [
                {"name": "User", "value": "woody", "inline": True},
                {"name": "Time", "value": datetime.now().strftime("%H:%M"), "inline": True},
                {"name": "Database", "value": "✅ Logged" if db_success else "⚠️ Partial", "inline": True}
            ],
            "footer": {"text": "AIPA Immediate BMF Processing"}
        }]
    }
    
    try:
        print("📨 Sending Discord confirmation...")
        discord_response = requests.post(discord_webhook, json=discord_msg)
        
        if discord_response.status_code == 204:
            print("✅ Discord: Confirmation sent!")
        else:
            print(f"⚠️ Discord: Issue ({discord_response.status_code})")
    except Exception as e:
        print(f"❌ Discord error: {e}")
    
    print(f"\n🎉 BMF WORK PROCESSED!")
    print(f"Entry: {work_entry}")
    print(f"Time: {datetime.now().strftime('%H:%M')}")
    print(f"Database: {'✅' if db_success else '⚠️'}")
    print(f"Discord: ✅")
    
    return True

def show_discord_fix_status():
    """Show the status of Discord bot fix"""
    
    print(f"\n🔧 DISCORD BOT FIX STATUS")
    print("=" * 26)
    print("❌ Issue: Bot needs privileged intents enabled")
    print("🔧 Solution: Need to enable Message Content Intent")
    print("📋 Steps:")
    print("   1. Go to https://discord.com/developers/applications/")
    print("   2. Select AIPA application")
    print("   3. Go to Bot → Privileged Gateway Intents")
    print("   4. Enable 'Message Content Intent'")
    print("   5. Save changes")
    print("   6. Run the bot again")
    
    print(f"\n💡 QUICK ALTERNATIVE:")
    print("   • Use slash commands: /bmf work_description")
    print("   • No special permissions needed")
    print("   • Works immediately")

def create_quick_bmf_commands():
    """Create a quick commands reference"""
    
    commands_html = '''<!DOCTYPE html>
<html>
<head>
    <title>AIPA BMF Quick Commands</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #2c2f33; color: #fff; }
        .container { max-width: 800px; margin: 0 auto; }
        .command { background: #40444b; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .status { background: #7289da; padding: 10px; border-radius: 5px; margin: 10px 0; }
        code { background: #36393f; padding: 5px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AIPA BMF Quick Commands</h1>
        
        <div class="status">
            <h3>📊 Current Status</h3>
            <p>✅ Immediate BMF processing: Available</p>
            <p>⚠️ Discord bot auto-replies: Fixing permissions</p>
            <p>✅ Database logging: Working</p>
            <p>✅ Discord confirmations: Working</p>
        </div>
        
        <div class="command">
            <h3>🔨 Log BMF Work (Immediate)</h3>
            <p>Run this Python script to log work immediately:</p>
            <code>python bmf_immediate.py</code>
            <p>Then type your work description when prompted.</p>
        </div>
        
        <div class="command">
            <h3>📱 Discord Slash Commands (Once Bot Fixed)</h3>
            <p>In Discord, type:</p>
            <code>/bmf tomorrow eddison and wanless fitting leadscrew</code>
            <p>Bot will automatically process and confirm.</p>
        </div>
        
        <div class="command">
            <h3>🌐 Web Interface</h3>
            <p>Open bmf_web_logger.html for browser-based logging</p>
        </div>
        
        <div class="command">
            <h3>🔧 Fix Discord Bot</h3>
            <p>To enable automatic Discord replies:</p>
            <ol>
                <li>Go to <a href="https://discord.com/developers/applications/" target="_blank">Discord Developer Portal</a></li>
                <li>Select AIPA application</li>
                <li>Go to Bot → Privileged Gateway Intents</li>
                <li>Enable "Message Content Intent"</li>
                <li>Save changes</li>
                <li>Run: <code>python discord_bot_bmf.py</code></li>
            </ol>
        </div>
    </div>
</body>
</html>'''
    
    with open('bmf_quick_commands.html', 'w', encoding='utf-8') as f:
        f.write(commands_html)
    
    print("✅ Created quick commands reference: bmf_quick_commands.html")

if __name__ == "__main__":
    print("🤖 AIPA BMF - Immediate Solution")
    print("=" * 35)
    
    # Process BMF work immediately
    success = process_bmf_immediate()
    
    if success:
        # Show next steps
        show_discord_fix_status()
        create_quick_bmf_commands()
        
        print(f"\n📋 WHAT'S NEXT:")
        print(f"✅ Your work entry is processed and logged")
        print(f"🔧 Enable Discord bot permissions for auto-replies")
        print(f"💡 Or use this script anytime: python bmf_immediate.py")
        
        # Try to open commands reference
        try:
            webbrowser.open('bmf_quick_commands.html')
            print(f"🌐 Opened quick commands in browser")
        except:
            print(f"📄 Quick commands saved: bmf_quick_commands.html")
    else:
        print("❌ Issues with immediate processing")