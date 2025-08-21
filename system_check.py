#!/usr/bin/env python3
"""
AdinavAI System Health Check
Quick diagnostic script to verify all components are working
"""

import requests
import subprocess
import sys
import os

def check_ollama_running():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_ollama_models():
    """Check what models are available"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        return 'gpt-oss:20b' in result.stdout
    except:
        return False

def check_python_dependencies():
    """Check if required Python packages are installed"""
    required = ['flask', 'requests', 'cryptography', 'pyttsx3']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def main():
    print("🔍 AdinavAI System Health Check")
    print("=" * 40)
    
    # Check Ollama
    if check_ollama_running():
        print("✅ Ollama server: RUNNING")
    else:
        print("❌ Ollama server: NOT RUNNING")
        print("   Run: ollama serve")
        return False
    
    # Check Model
    if check_ollama_models():
        print("✅ gpt-oss:20b model: AVAILABLE")
    else:
        print("❌ gpt-oss:20b model: NOT FOUND")
        print("   Run: ollama pull gpt-oss:20b")
        return False
    
    # Check Dependencies
    missing = check_python_dependencies()
    if not missing:
        print("✅ Python dependencies: ALL INSTALLED")
    else:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print(f"   Run: pip install {' '.join(missing)}")
        return False
    
    # Test AI Connection
    try:
        sys.path.append('agents')
        from ai_powered_chat_agent import AIPoweredFamilyChatAgent
        agent = AIPoweredFamilyChatAgent()
        if agent.test_ai_connection():
            print("✅ AI Agent connection: WORKING")
        else:
            print("❌ AI Agent connection: FAILED")
            return False
    except Exception as e:
        print(f"❌ AI Agent test: ERROR - {e}")
        return False
    
    print("\n🎉 All systems operational!")
    print("   You can now run: python family_app.py")
    return True

if __name__ == "__main__":
    main()
