#!/usr/bin/env python3
"""
AdinavAI Family System - Smart Startup Script
Handles Ollama startup, directory navigation, and app launching
"""

import subprocess
import sys
import os
import time
import requests
import socket
from pathlib import Path

def find_free_port():
    """Find a free port starting from 8080"""
    for port in [8080, 5000, 3000, 8000, 8888, 9000]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except OSError:
                continue
    return 8080

def check_ollama_running():
    """Check if Ollama is already running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=3)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Start Ollama if not already running"""
    if check_ollama_running():
        print("✅ Ollama is already running")
        return True
    
    print("🚀 Starting Ollama server...")
    try:
        # Start Ollama in background
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Wait for it to start
        for i in range(10):
            time.sleep(1)
            if check_ollama_running():
                print("✅ Ollama started successfully")
                return True
            print(f"⏳ Waiting for Ollama... ({i+1}/10)")
        
        print("❌ Ollama failed to start")
        return False
        
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        return False

def check_models():
    """Check if required models are available"""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if 'gpt-oss:20b' in result.stdout:
            print("✅ gpt-oss:20b model is available")
            return True
        else:
            print("❌ gpt-oss:20b model not found")
            print("   Run: ollama pull gpt-oss:20b")
            return False
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False

def start_family_app():
    """Start the family application"""
    # Ensure we're in the correct directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    port = find_free_port()
    os.environ['PORT'] = str(port)
    
    print(f"🌐 Starting AdinavAI Family App on port {port}...")
    print(f"   Local: http://localhost:{port}")
    print(f"   Mobile: http://192.168.1.156:{port}")
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, 'family_app.py'])
    except KeyboardInterrupt:
        print("\n🛑 AdinavAI stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        print("   Trying simple mode...")
        try:
            subprocess.run([sys.executable, 'family_app_simple.py'])
        except Exception as e2:
            print(f"❌ Simple mode also failed: {e2}")

def main():
    print("=" * 60)
    print("🤖 AdinavAI Family System - Smart Startup")
    print("=" * 60)
    
    # Step 1: Ensure Ollama is running
    if not start_ollama():
        print("\n❌ Cannot start without Ollama")
        print("   Please install Ollama: https://ollama.ai")
        return False
    
    # Step 2: Check models
    if not check_models():
        print("\n⚠️ AI features will be limited")
        print("   Run: ollama pull gpt-oss:20b")
    
    # Step 3: Start the application
    print("\n🎯 Starting AdinavAI Family App...")
    start_family_app()
    
    return True

if __name__ == "__main__":
    main()