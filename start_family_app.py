"""
AdinavAI Family App Launcher
Quick start script for the complete family application
"""

import os
import sys
import subprocess

def banner():
    """Display startup banner"""
    print("\n" + "=" * 80)
    print("🏠 AdinavAI Family App - Complete System")
    print("=" * 80)
    print("📱 Features:")
    print("  ✓ Family member login system")
    print("  ✓ Mobile-responsive design") 
    print("  ✓ AI-powered conversations (GPT-OSS 20B)")
    print("  ✓ Voice interaction (speech-to-text)")
    print("  ✓ Personalized responses for each family member")
    print("  ✓ Memory of family conversations")
    print("  ✓ Secure family authentication")
    print("\n👨‍👩‍👧‍👦 Family Credentials:")
    print("  • Santosh (Papa): papa123")
    print("  • Maryne (Mama): mama123")
    print("  • Aditya: aditya123") 
    print("  • Avinav: avinav123")
    print("=" * 80)

def check_dependencies():
    """Check if required packages are installed"""
    print("🔧 Checking dependencies...")
    
    required_packages = ["flask", "requests"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package} - Not installed")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✓ All packages installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_ai_model():
    """Check if Ollama and gpt-oss:20b are available"""
    print("\n🧠 Checking AI model availability...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            model_names = [model['name'] for model in models.get('models', [])]
            
            if 'gpt-oss:20b' in model_names:
                print("  ✓ Ollama is running")
                print("  ✓ gpt-oss:20b model is available")
                return True
            else:
                print("  ✓ Ollama is running")
                print("  ❌ gpt-oss:20b model not found")
                print("    Available models:", model_names)
                print("    Run: ollama pull gpt-oss:20b")
                return False
        else:
            print("  ❌ Ollama not responding")
            return False
    except:
        print("  ❌ Cannot connect to Ollama")
        print("    Make sure Ollama is running")
        return False

def start_application():
    """Start the family application"""
    print("\n🚀 Starting AdinavAI Family App...")
    
    try:
        # Run the family app
        from family_app import app
        
        print("🌐 Family app is running at:")
        print("   http://localhost:5000")
        print("   (Access from your phone using your computer's IP address)")
        print("\n💡 Tips:")
        print("   • Works great on mobile phones")
        print("   • Each family member can login with their credentials")
        print("   • Try the voice input feature (🎤 button)")
        print("   • AdinavAI remembers all family conversations")
        print("\n" + "=" * 80)
        
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return False

def main():
    """Main launcher function"""
    banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please fix and try again.")
        return
    
    # Check AI model
    ai_available = check_ai_model()
    if not ai_available:
        print("\n⚠️  AI model not ready, but starting app anyway.")
        print("   Basic features will work, AI responses will be fallback messages.")
        input("\nPress Enter to continue or Ctrl+C to cancel...")
    
    # Start the application
    start_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 AdinavAI Family App stopped. See you soon!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check the logs and try again.")