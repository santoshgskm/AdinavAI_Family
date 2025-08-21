"""
AdinavAI Family System Launcher
Simple script to start your family's AI assistant
"""

import os
import sys
import subprocess
import json

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        print("Flask is installed")
        return True
    except ImportError:
        print("Flask not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("Flask installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install Flask. Please install manually: pip install flask")
            return False

def create_family_data_if_needed():
    """Create family data directory and files if they don't exist"""
    data_dir = "family_data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created {data_dir} directory")
    
    # Create family members file if it doesn't exist
    family_file = os.path.join(data_dir, "family_members.json")
    if not os.path.exists(family_file):
        family_data = {
            "family": {
                "name": "Gupta Family",
                "created": "2025-01-20",
                "values": ["love", "learning", "growth", "privacy", "togetherness"]
            },
            "members": {
                "santosh": {
                    "name": "Santosh",
                    "role": "father",
                    "interests": ["AI", "quantum computing", "family", "learning", "dreams"],
                    "personality": "curious, loving, ambitious, dedicated family man",
                    "conversation_history": [],
                    "preferences": {},
                    "memories": []
                },
                "maryne": {
                    "name": "Maryne",
                    "role": "mother",
                    "interests": [],
                    "personality": "to_be_learned",
                    "conversation_history": [],
                    "preferences": {},
                    "memories": []
                },
                "aditya": {
                    "name": "Aditya",
                    "role": "son",
                    "age_group": "child",
                    "interests": [],
                    "personality": "to_be_learned",
                    "conversation_history": [],
                    "preferences": {},
                    "memories": []
                },
                "avinav": {
                    "name": "Avinav", 
                    "role": "son",
                    "age_group": "child",
                    "interests": [],
                    "personality": "to_be_learned",
                    "conversation_history": [],
                    "preferences": {},
                    "memories": []
                }
            },
            "family_memories": {
                "shared_experiences": [],
                "traditions": [],
                "important_dates": {},
                "family_stories": []
            }
        }
        
        with open(family_file, 'w', encoding='utf-8') as f:
            json.dump(family_data, f, indent=2, ensure_ascii=False)
        print(f"Created {family_file}")

def start_family_ai():
    """Start the AdinavAI family system"""
    print("Starting AdinavAI Family System...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("Please install required packages first")
        return
    
    # Create data directories
    create_family_data_if_needed()
    
    # Start the web interface
    print("\nAdinavAI is starting up...")
    print("This AI is named after Aditya and Avinav")
    print("Created with love for the Gupta family")
    print("\nOpen your web browser and go to:")
    print("   http://localhost:5000")
    print("\nEach family member can now chat with AdinavAI!")
    print("AdinavAI will remember everything about your family")
    print("\n" + "=" * 50)
    
    # Change to web interface directory and start
    web_dir = "web_interface"
    if os.path.exists(web_dir):
        os.chdir(web_dir)
        try:
            # Import and run the Flask app
            sys.path.append('.')
            from app import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except Exception as e:
            print(f"Error starting web interface: {e}")
    else:
        print(f"Web interface directory '{web_dir}' not found")

if __name__ == "__main__":
    start_family_ai()