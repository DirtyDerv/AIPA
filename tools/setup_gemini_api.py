#!/usr/bin/env python3
"""
Gemini API Key Configuration Helper
Automatically configures your Gemini API key in the n8n workflow
"""

import requests
import json

# Configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk"
GEMINI_WORKFLOW_ID = "YXFT5s6U3HD5qarc"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def setup_gemini_api_key():
    """Guide user through Gemini API key setup"""
    
    print("🔮 AIPA Gemini API Key Setup")
    print("=" * 40)
    
    print("\n📋 Step 1: Get Your Gemini API Key")
    print("1. Go to: https://aistudio.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the generated API key")
    
    gemini_api_key = input("\n🔑 Enter your Gemini API key: ").strip()
    
    if not gemini_api_key:
        print("❌ No API key provided. Exiting.")
        return False
    
    if not gemini_api_key.startswith('AI'):
        print("⚠️ Warning: Gemini API keys usually start with 'AI'. Please verify your key.")
    
    print(f"\n🔄 Configuring Gemini API key in n8n workflow...")
    
    try:
        # Get the current workflow
        response = requests.get(f"{N8N_URL}/api/v1/workflows/{GEMINI_WORKFLOW_ID}", headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Failed to get workflow: {response.status_code}")
            return False
        
        workflow = response.json()
        
        # Update nodes with Gemini API key
        nodes_updated = 0
        for node in workflow.get('nodes', []):
            if 'gemini' in node.get('name', '').lower():
                # Update query parameters for Gemini API calls
                if 'parameters' in node and 'queryParameters' in node['parameters']:
                    for param in node['parameters']['queryParameters'].get('parameters', []):
                        if param.get('name') == 'key':
                            param['value'] = gemini_api_key
                            nodes_updated += 1
        
        if nodes_updated == 0:
            print("⚠️ No Gemini API nodes found to update. Manual configuration may be needed.")
            print("\n📋 Manual Setup Instructions:")
            print("1. Go to n8n: http://192.168.0.14:5678")
            print("2. Open workflow: 'AIPA - Discord Voice & File Processor (Gemini)'")
            print("3. Edit nodes: 'Gemini Text Analysis' and 'Gemini Image Analysis'")
            print(f"4. Replace 'YOUR_GEMINI_API_KEY' with: {gemini_api_key}")
            return True
        
        # Save the updated workflow
        update_response = requests.put(f"{N8N_URL}/api/v1/workflows/{GEMINI_WORKFLOW_ID}", 
                                     headers=headers, json=workflow)
        
        if update_response.status_code == 200:
            print(f"✅ Successfully configured Gemini API key!")
            print(f"📊 Updated {nodes_updated} workflow nodes")
            return True
        else:
            print(f"❌ Failed to update workflow: {update_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error configuring API key: {e}")
        return False

def test_gemini_integration():
    """Test if Gemini integration is working"""
    
    print("\n🧪 Testing Gemini Integration")
    print("=" * 35)
    
    gemini_api_key = input("🔑 Enter your Gemini API key to test: ").strip()
    
    if not gemini_api_key:
        print("❌ No API key provided for testing.")
        return False
    
    # Test Gemini API directly
    test_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    test_headers = {"Content-Type": "application/json"}
    test_params = {"key": gemini_api_key}
    test_data = {
        "contents": [{
            "parts": [{
                "text": "Hello! Please respond with 'AIPA Gemini integration test successful' to confirm the API is working."
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 100
        }
    }
    
    try:
        response = requests.post(test_url, headers=test_headers, params=test_params, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ Gemini API Test Successful!")
                print(f"🤖 Gemini Response: {ai_response}")
                return True
            else:
                print(f"⚠️ Unexpected API response format: {result}")
                return False
        else:
            print(f"❌ API Test Failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini API: {e}")
        return False

def main():
    """Main setup function"""
    
    print("🔮 Welcome to AIPA Gemini Setup!")
    print("This will help you configure Google Gemini for your Discord bot.")
    
    while True:
        print("\n📋 Choose an option:")
        print("1. Setup Gemini API key in n8n workflow")
        print("2. Test Gemini API integration")
        print("3. View setup instructions")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            success = setup_gemini_api_key()
            if success:
                print("\n🎉 Gemini API key configured successfully!")
                print("🚀 Your Discord bot is now ready to use Gemini AI!")
        
        elif choice == '2':
            success = test_gemini_integration()
            if success:
                print("\n🎊 Gemini integration is working perfectly!")
        
        elif choice == '3':
            print("\n📋 Gemini Setup Instructions:")
            print("1. Get API key: https://aistudio.google.com/app/apikey")
            print("2. Configure in n8n workflow (option 1)")
            print("3. Test integration (option 2)")
            print("4. Start using voice/image features in Discord!")
            
            print("\n🔮 Gemini Features:")
            print("• Text analysis and conversation")
            print("• Image analysis and description")
            print("• Document processing")
            print("• Voice file handling")
            print("• Fast response times")
            print("• Generous free tier")
        
        elif choice == '4':
            print("\n👋 Thanks for using AIPA Gemini setup!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()