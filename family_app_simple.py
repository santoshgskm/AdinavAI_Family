"""
AdinavAI Simple Family App - Version sans AI pour test
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import hashlib
import datetime
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'AdinavAI_Family_Secret_2025')

# Family credentials
FAMILY_USERS = {
    "santosh": {
        "password": hashlib.sha256("santosh2025".encode()).hexdigest(),
        "display_name": "Santosh Gupta",
        "role": "admin",
        "avatar": "👨‍💼"
    },
    "maryne": {
        "password": hashlib.sha256("maryne2025".encode()).hexdigest(),
        "display_name": "Maryne Gupta", 
        "role": "mother",
        "avatar": "👩‍💼"
    },
    "aditya": {
        "password": hashlib.sha256("aditya2025".encode()).hexdigest(),
        "display_name": "Aditya Gupta",
        "role": "son",
        "avatar": "👦"
    },
    "avinav": {
        "password": hashlib.sha256("avinav2025".encode()).hexdigest(),
        "display_name": "Avinav Gupta",
        "role": "son", 
        "avatar": "👦"
    }
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('family_chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json or {}
        username = data.get('username', '').lower()
        password = data.get('password', '')
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if username in FAMILY_USERS and FAMILY_USERS[username]['password'] == password_hash:
            session['username'] = username
            session['display_name'] = FAMILY_USERS[username]['display_name']
            session['role'] = FAMILY_USERS[username]['role']
            session['avatar'] = FAMILY_USERS[username]['avatar']
            
            return jsonify({
                'success': True,
                'message': f'Bienvenue, {FAMILY_USERS[username]["display_name"]}!',
                'redirect': '/chat'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Nom d\'utilisateur ou mot de passe incorrect.'
            }), 401
    
    return render_template('family_login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/chat')
@login_required
def family_chat():
    return render_template('family_chat_app.html', user=session)

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    try:
        data = request.json or {}
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Aucun message fourni'}), 400
        
        # Simple response without AI for testing
        responses = [
            f"Salut {session['display_name']} ! J'ai reçu votre message : '{message}'",
            f"Bonjour ! AdinavAI fonctionne correctement. Vous avez dit : {message}",
            f"Test réussi ! Votre message '{message}' a été reçu par AdinavAI.",
        ]
        
        import random
        response = random.choice(responses)
        
        return jsonify({
            'user_message': message,
            'ai_response': response,
            'timestamp': datetime.datetime.now().strftime("%H:%M"),
            'user': session['display_name'],
            'avatar': session['avatar']
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Erreur interne',
            'ai_response': f"Désolé {session.get('display_name', '')}, j'ai une petite difficulté technique !"
        }), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'ai_connected': False,  # Simple mode
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 70)
    print("AdinavAI Simple Family App (Mode Test)")
    print("=" * 70)
    
    print("\\nIdentifiants de test:")
    print("- santosh: santosh2025")
    print("- maryne: maryne2025") 
    print("- aditya: aditya2025")
    print("- avinav: avinav2025")
    
    port = int(os.environ.get('PORT', 8080))
    print(f"\\nAccédez à l'application:")
    print(f"   http://localhost:{port}")
    print(f"   http://192.168.1.156:{port} (mobile)")
    print("=" * 70)
    
    try:
        print(f"\\nDémarrage du serveur sur le port {port}...")
        app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {port} occupé, essai port {port + 1}")
            app.run(debug=False, host='0.0.0.0', port=port + 1, threaded=True)
        else:
            print(f"Erreur: {e}")