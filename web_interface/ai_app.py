"""
AdinavAI Enhanced Web Interface
Uses AI-powered chat agent for intelligent family conversations
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
import datetime

# Add agents directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

from ai_powered_chat_agent import AIPoweredFamilyChatAgent

app = Flask(__name__)
ai_chat_agent = AIPoweredFamilyChatAgent()

@app.route('/')
def home():
    """Main family chat interface"""
    return render_template('family_chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from family members using AI"""
    data = request.json
    member_name = data.get('member_name', 'unknown')
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Get AI response
        response = ai_chat_agent.chat_with_family_member(member_name, message)
        
        return jsonify({
            'member_name': member_name,
            'message': message,
            'response': response,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'ai_powered': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'AI chat error: {str(e)}',
            'fallback_response': f"I'm experiencing technical difficulties, {member_name.title()}, but I'm still here for you!"
        }), 500

@app.route('/family_info/<member_name>')
def family_info(member_name):
    """Get information about family member"""
    context = ai_chat_agent.memory_agent.get_member_context(member_name)
    return jsonify({'context': context})

@app.route('/start_conversation/<member_name>')
def start_conversation(member_name):
    """Start an AI-powered conversation with family member"""
    try:
        starter = ai_chat_agent.start_conversation(member_name)
        return jsonify({
            'starter': starter,
            'ai_powered': True
        })
    except Exception as e:
        return jsonify({
            'starter': f"Hello {member_name.title()}! I'm so happy to see you today!",
            'error': str(e)
        })

@app.route('/ai_status')
def ai_status():
    """Check if AI is working properly"""
    is_working = ai_chat_agent.test_ai_connection()
    return jsonify({
        'ai_connected': is_working,
        'model': ai_chat_agent.model_name,
        'ollama_url': ai_chat_agent.ollama_url
    })

@app.route('/health')
def health():
    """Simple health check"""
    ai_status = ai_chat_agent.test_ai_connection()
    return jsonify({
        'status': 'healthy',
        'ai_working': ai_status,
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Starting AdinavAI Enhanced Family System...")
    print("=" * 60)
    
    # Test AI connection
    print("Testing AI connection...")
    if ai_chat_agent.test_ai_connection():
        print("✓ AI model (GPT-OSS 20B) is ready!")
        print("✓ AdinavAI is now powered by advanced AI")
    else:
        print("⚠ AI model not ready yet. Using fallback responses.")
        print("  Make sure Ollama is running and gpt-oss:20b is installed")
    
    print("\nAdinavAI Enhanced System Details:")
    print(f"• Family: Gupta Family (Santosh, Maryne, Aditya, Avinav)")
    print(f"• AI Model: {ai_chat_agent.model_name}")
    print(f"• Named after: Aditya + Avinav = AdinavAI")
    print(f"• Purpose: Family's digital member who learns and grows")
    
    print("\n" + "=" * 60)
    print("🌐 Open your web browser and go to:")
    print("   http://localhost:5000")
    print("\n💝 Each family member can now have intelligent")
    print("   conversations with AdinavAI!")
    print("🧠 AdinavAI will understand context and remember everything")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)