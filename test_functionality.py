#!/usr/bin/env python3
"""
AdinavAI Functionality Test Script
Tests all components to ensure everything is working
"""

import requests
import json
import time

def test_ollama():
    """Test Ollama connection"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama: Connected")
            return True
        else:
            print("❌ Ollama: Connection failed")
            return False
    except Exception as e:
        print(f"❌ Ollama: Error - {e}")
        return False

def test_web_app():
    """Test web application"""
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✅ Web App: Running")
            return True
        else:
            print("❌ Web App: Not responding")
            return False
    except Exception as e:
        print(f"❌ Web App: Error - {e}")
        return False

def test_login():
    """Test login functionality"""
    try:
        login_data = {
            "username": "santosh",
            "password": "santosh2025"
        }
        
        # Create a session to maintain cookies
        session = requests.Session()
        
        # Login
        response = session.post(
            "http://localhost:8080/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Login: Successful")
                return session
            else:
                print(f"❌ Login: Failed - {data.get('message', 'Unknown error')}")
                return None
        else:
            print(f"❌ Login: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Login: Error - {e}")
        return None

def test_chat(session):
    """Test chat functionality"""
    try:
        chat_data = {
            "message": "Hello AdinavAI, this is a test message."
        }
        
        response = session.post(
            "http://localhost:8080/api/chat",
            json=chat_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'ai_response' in data:
                print("✅ Chat: Working")
                print(f"   AI Response: {data['ai_response'][:100]}...")
                return True
            else:
                print(f"❌ Chat: No AI response - {data}")
                return False
        else:
            print(f"❌ Chat: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Chat: Error - {e}")
        return False

def test_voice_capabilities(session):
    """Test voice capabilities"""
    try:
        response = session.get("http://localhost:8080/api/voice-capabilities", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Voice: Capabilities available")
                return True
            else:
                print(f"❌ Voice: Capabilities failed - {data}")
                return False
        else:
            print(f"❌ Voice: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Voice: Error - {e}")
        return False

def main():
    print("🔍 AdinavAI Functionality Test")
    print("=" * 40)
    
    # Test 1: Ollama
    if not test_ollama():
        print("\n❌ Cannot continue without Ollama")
        return False
    
    # Test 2: Web App
    if not test_web_app():
        print("\n❌ Cannot continue without web app")
        return False
    
    # Test 3: Login
    session = test_login()
    if not session:
        print("\n❌ Cannot continue without login")
        return False
    
    # Test 4: Chat
    if not test_chat(session):
        print("\n❌ Chat functionality not working")
        return False
    
    # Test 5: Voice
    test_voice_capabilities(session)
    
    print("\n🎉 All core functionality tests completed!")
    print("\n📝 Next Steps:")
    print("1. Open http://localhost:8080 in your browser")
    print("2. Login with santosh / santosh2025")
    print("3. Try sending a message")
    print("4. Test voice features")
    
    return True

if __name__ == "__main__":
    main()
