#!/usr/bin/env python3
"""
Quick Test for Discord NLP Workflow
"""

import requests
import json

def test_nlp_workflow():
    """Test the n8n Discord NLP workflow"""

    test_message = "can you enter a note for work today the parts for eddidson and waneless are back at cannons"

    payload = {
        "content": test_message,
        "author": {"username": "test_user"},
        "channel_id": "123456789",
        "timestamp": "2024-01-01T12:00:00Z"
    }

    print("🧪 Testing Discord NLP Workflow")
    print(f"📝 Message: {test_message}")
    print("🔗 Endpoint: http://localhost:5678/webhook/discord-nlp")
    print("-" * 50)

    try:
        response = requests.post(
            "http://localhost:5678/webhook/discord-nlp",
            json=payload,
            timeout=15
        )

        print(f"📊 Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"🎯 Intent: {result.get('intent', 'unknown')}")
            print(f"📁 Category: {result.get('category', 'unknown')}")
            print(f"📝 Content: {result.get('extracted_data', {}).get('description', 'N/A')[:100]}...")
        else:
            print(f"❌ Error: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Cannot reach n8n server")
        print("💡 Make sure n8n is running at http://localhost:5678")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_nlp_workflow()