#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse

class BMFHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get the content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            
            # Process BMF work entry
            content = data.get('content', '')
            author = data.get('author', {}).get('username', 'woody')
            
            if 'bmf work:' in content.lower():
                # Extract work description
                work_desc = content.split('bmf work:', 1)[1].strip()
                
                print(f"📝 Processing BMF work: {work_desc}")
                
                # Log to Supabase
                supabase_url = "https://neoeoabqcfpopzkwvcxq.supabase.co/rest/v1/conversations"
                supabase_headers = {
                    'Content-Type': 'application/json',
                    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck',
                    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck',
                    'Prefer': 'return=minimal'
                }
                
                supabase_data = {
                    'user_id': author,
                    'message': work_desc,
                    'business_context': 'bmf-work',
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'message_type': 'work_log'
                }
                
                try:
                    db_response = requests.post(supabase_url, json=supabase_data, headers=supabase_headers)
                    print(f"Database log: {db_response.status_code}")
                except Exception as e:
                    print(f"Database error: {e}")
                
                # Send Discord confirmation
                discord_webhook = "https://discord.com/api/webhooks/1434598843546341581/r0NqE35ekv_88zWCj7TYze_15zuKtN_wsARtWMesa-_KVkKPA26jkZNNlSC2_3G4grzf"
                discord_data = {
                    "embeds": [{
                        "title": "✅ BMF Work Logged",
                        "description": work_desc,
                        "color": 16753920,
                        "fields": [
                            {"name": "User", "value": author, "inline": True},
                            {"name": "Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M"), "inline": True},
                            {"name": "Type", "value": "Work Log Entry", "inline": True}
                        ],
                        "footer": {"text": "BMF Direct Integration"}
                    }]
                }
                
                try:
                    discord_response = requests.post(discord_webhook, json=discord_data)
                    print(f"Discord confirmation: {discord_response.status_code}")
                except Exception as e:
                    print(f"Discord error: {e}")
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "success"}')
                
                return
        
        except Exception as e:
            print(f"Error processing request: {e}")
            self.send_response(500)
            self.end_headers()
            
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def start_bmf_server():
    server = HTTPServer(('localhost', 8765), BMFHandler)
    print("🚀 BMF Direct Integration Server running on http://localhost:8765")
    print("📝 Send POST requests with BMF work entries")
    server.serve_forever()

if __name__ == "__main__":
    start_bmf_server()
