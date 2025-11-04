#!/usr/bin/env python3
"""
Test Advanced Discord NLP Workflow
"""

import requests
import json
from datetime import datetime

def test_nlp_message(message_content, author_name="TestUser"):
    """Test the advanced NLP workflow with a message"""

    print(f"🧪 Testing NLP: {message_content}")

    # Prepare test data in Discord format
    test_data = {
        "content": message_content,
        "author": {
            "username": author_name,
            "id": "123456789"
        },
        "channel_id": "987654321",
        "timestamp": datetime.now().isoformat()
    }

    try:
        response = requests.post(
            "http://localhost:5678/webhook/discord-nlp-advanced",
            json=test_data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ NLP Response:")
            print(f"   Content: {result.get('content', 'No content')}")
            return True
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧠 Testing Advanced Discord NLP Workflow")
    print("=" * 50)

    # Test various message types
    test_messages = [
        "Add a note about meeting with client tomorrow",
        "I worked 4 hours on the website project",
        "What's the status of the DJ booking for Saturday?",
        "Create a note: Call supplier about delivery delay",
        "Log 2.5 hours working on BMF project",
        "How many hours did I work this week?"
    ]

    for msg in test_messages:
        test_nlp_message(msg)
        print("-" * 30)

    print("🎯 Test complete! Check results above.")