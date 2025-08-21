"""
AdinavAI Family Web Interface
Simple web app for family to chat with AdinavAI
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add agents directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

from family_chat_agent import FamilyChatAgent

app = Flask(__name__)
chat_agent = FamilyChatAgent()

@app.route('/')
def home():
    """Main family chat interface"""
    return render_template('family_chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from family members"""
    data = request.json
    member_name = data.get('member_name', 'unknown')
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get response from AdinavAI
    response = chat_agent.chat_with_family_member(member_name, message)
    
    return jsonify({
        'member_name': member_name,
        'message': message,
        'response': response,
        'timestamp': 'now'
    })

@app.route('/family_info/<member_name>')
def family_info(member_name):
    """Get information about family member"""
    context = chat_agent.memory_agent.get_member_context(member_name)
    return jsonify({'context': context})

@app.route('/start_conversation/<member_name>')
def start_conversation(member_name):
    """Start a conversation with family member"""
    starter = chat_agent.start_conversation(member_name)
    return jsonify({'starter': starter})

if __name__ == '__main__':
    print("Starting AdinavAI Family Web Interface...")
    print("Open your browser and go to: http://localhost:5000")
    print("Family members can now chat with AdinavAI!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)