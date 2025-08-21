"""
Test script for AdinavAI AI Upgrade
Verifies the GPT-OSS 20B integration is working
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from ai_powered_chat_agent import AIPoweredFamilyChatAgent

def test_ollama_connection():
    """Test basic Ollama connection"""
    print("🔧 Testing Ollama connection...")
    
    import requests
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            print("✓ Ollama is running")
            
            # Check if gpt-oss:20b is available
            model_names = [model['name'] for model in models.get('models', [])]
            if 'gpt-oss:20b' in model_names:
                print("✓ gpt-oss:20b model is available")
                return True
            else:
                print("❌ gpt-oss:20b model not found")
                print(f"Available models: {model_names}")
                return False
        else:
            print("❌ Ollama not responding")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_ai_agent():
    """Test the AI-powered family chat agent"""
    print("\n🤖 Testing AI-powered family chat agent...")
    
    try:
        # Create agent
        ai_agent = AIPoweredFamilyChatAgent()
        
        # Test connection
        if ai_agent.test_ai_connection():
            print("✓ AI agent connection successful!")
            
            # Test conversation with Santosh
            print("\n💬 Testing conversation with Santosh:")
            response = ai_agent.chat_with_family_member(
                "santosh", 
                "Hello AdinavAI! How are you today?"
            )
            print(f"AdinavAI: {response}")
            
            # Test with context understanding
            print("\n🧠 Testing context understanding:")
            response = ai_agent.chat_with_family_member(
                "santosh",
                "What do you know about our family?"
            )
            print(f"AdinavAI: {response}")
            
            return True
        else:
            print("❌ AI agent connection failed")
            return False
            
    except Exception as e:
        print(f"❌ AI agent test failed: {e}")
        return False

def test_family_memory_integration():
    """Test that family memory is working with AI"""
    print("\n🧠 Testing family memory integration...")
    
    try:
        ai_agent = AIPoweredFamilyChatAgent()
        
        # Check if family data is loaded
        family_context = ai_agent.memory_agent.get_family_context()
        print("✓ Family context loaded:")
        print(f"  {family_context.split(chr(10))[0]}")  # First line
        
        # Check member context
        santosh_context = ai_agent.memory_agent.get_member_context("santosh")
        print("✓ Santosh context available:")
        print(f"  Interests: {santosh_context.split('Interests: ')[1].split(chr(10))[0] if 'Interests: ' in santosh_context else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 AdinavAI AI Upgrade Test Suite")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Ollama Connection
    if test_ollama_connection():
        tests_passed += 1
    
    # Test 2: AI Agent
    if test_ai_agent():
        tests_passed += 1
    
    # Test 3: Memory Integration
    if test_family_memory_integration():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! AdinavAI is ready for AI-powered conversations!")
        print("\n🌟 Your family can now enjoy:")
        print("  • Intelligent, context-aware conversations")
        print("  • Personalized responses for each family member")
        print("  • Better understanding of family dynamics")
        print("  • Improved memory of family preferences and interests")
        
        print("\n▶️  To start the enhanced AdinavAI:")
        print("    cd web_interface")
        print("    python ai_app.py")
        
    else:
        print("❌ Some tests failed. Check the output above for details.")
        
        if tests_passed == 0:
            print("\n🔍 Troubleshooting:")
            print("  • Make sure Ollama is running")
            print("  • Verify gpt-oss:20b download completed:")
            print("    ollama list")
            print("  • If needed, re-download the model:")
            print("    ollama pull gpt-oss:20b")
    
    print("=" * 60)

if __name__ == "__main__":
    main()