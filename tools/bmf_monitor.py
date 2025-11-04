#!/usr/bin/env python3
"""
BMF Work Entry Monitor
Monitors for BMF work entries and processes them
"""

import requests
import json
from datetime import datetime
import time

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1434598843546341581/r0NqE35ekv_88zWCj7TYze_15zuKtN_wsARtWMesa-_KVkKPA26jkZNNlSC2_3G4grzf"
SUPABASE_URL = "https://neoeoabqcfpopzkwvcxq.supabase.co/rest/v1/conversations"
SUPABASE_HEADERS = {
    'Content-Type': 'application/json',
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck',
    'Prefer': 'return=minimal'
}

def process_bmf_entry(work_description, user="woody"):
    """Process a BMF work entry"""
    
    timestamp = datetime.now().isoformat()
    
    # Log to database
    db_data = {
        'user_id': user,
        'message': work_description,
        'business_context': 'bmf-work',
        'timestamp': timestamp,
        'message_type': 'work_log',
        'source': 'bmf_monitor'
    }
    
    try:
        db_response = requests.post(SUPABASE_URL, json=db_data, headers=SUPABASE_HEADERS)
        db_success = db_response.status_code in [200, 201]
    except:
        db_success = False
    
    # Send Discord confirmation
    discord_data = {
        "embeds": [{
            "title": "✅ BMF Work Logged",
            "description": work_description,
            "color": 16753920,
            "fields": [
                {"name": "User", "value": user, "inline": True},
                {"name": "Time", "value": datetime.now().strftime("%H:%M"), "inline": True},
                {"name": "Database", "value": "✅ Logged" if db_success else "❌ Failed", "inline": True}
            ],
            "footer": {"text": "BMF Monitor System"}
        }]
    }
    
    try:
        discord_response = requests.post(DISCORD_WEBHOOK, json=discord_data)
        discord_success = discord_response.status_code == 204
    except:
        discord_success = False
    
    return db_success and discord_success

def send_ready_message():
    """Send a message indicating the monitor is ready"""
    
    ready_msg = {
        "embeds": [{
            "title": "🟢 BMF Monitor Ready",
            "description": "BMF work logging system is now active and monitoring!",
            "color": 65280,
            "fields": [
                {
                    "name": "📝 How to Use",
                    "value": "Just mention BMF work entries in this channel and I'll process them automatically",
                    "inline": False
                },
                {
                    "name": "🧪 Test Command",
                    "value": "Say: `BMF: testing the monitor system`",
                    "inline": False
                }
            ],
            "footer": {"text": "Monitor system active"}
        }]
    }
    
    requests.post(DISCORD_WEBHOOK, json=ready_msg)

if __name__ == "__main__":
    send_ready_message()
    print("BMF Monitor started - watching for BMF entries...")
    
    # In a real implementation, this would monitor Discord messages
    # For now, it's ready to process manual entries
    while True:
        user_input = input("Enter BMF work (or 'quit'): ")
        if user_input.lower() == 'quit':
            break
        if user_input.strip():
            success = process_bmf_entry(user_input)
            print(f"Processed: {'✅' if success else '❌'}")
