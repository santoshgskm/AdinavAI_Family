"""
AdinavAI Complete Family App
- User authentication for each family member
- Mobile-responsive design
- Voice interaction capabilities
- Single interface for all family members
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sys
import os
import hashlib
import datetime
import logging
import sqlite3
from functools import wraps
from cryptography.fernet import Fernet

# Add agents directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))
from ai_powered_chat_agent import AIPoweredFamilyChatAgent
from voice_handler import VoiceHandler

app = Flask(__name__)

def get_or_create_flask_secret_key():
    """Persist a stable Flask secret key to avoid session resets across restarts"""
    key_file = os.path.join("family_data", "flask_secret.key")
    os.makedirs("family_data", exist_ok=True)
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    # prefer env var if provided; else generate and persist
    env_key = os.environ.get("FLASK_SECRET_KEY")
    if env_key:
        key_bytes = env_key.encode() if isinstance(env_key, str) else env_key
    else:
        key_bytes = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key_bytes)
    return key_bytes

app.secret_key = get_or_create_flask_secret_key()

# Initialize AI agent and voice handler
ai_chat_agent = AIPoweredFamilyChatAgent()
voice_handler = VoiceHandler()

# Family credentials - Secure storage with encrypted passwords
FAMILY_USERS = {
    "santosh": {
        "password": hashlib.sha256("santosh2025".encode()).hexdigest(),
        "display_name": "Santosh Gupta",
        "role": "admin",  # Only admin has full access
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
    },
    "sushma": {
        "password": hashlib.sha256("sushma2025".encode()).hexdigest(),
        "display_name": "Sushma Potlapally",
        "role": "sister",
        "avatar": "👩‍🦰"
    },
    "meghna": {
        "password": hashlib.sha256("meghna2025".encode()).hexdigest(),
        "display_name": "Meghna Potlapally",
        "role": "niece",
        "avatar": "👧"
    }
}

# Secure Data Storage Configuration
class SecureDataManager:
    def __init__(self):
        self.db_path = "family_data/secure_conversations.db"
        self.encryption_key = self.get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        self._connection_pool = {}
        self.init_database()
        self.setup_logging()
    
    def get_or_create_encryption_key(self):
        """Get or create encryption key for securing family data"""
        key_file = "family_data/encryption.key"
        
        # Create family_data directory if it doesn't exist
        os.makedirs("family_data", exist_ok=True)
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new encryption key
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def init_database(self):
        """Initialize secure SQLite database for conversations"""
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        cursor = conn.cursor()

        # Apply recommended PRAGMAs for concurrent web access
        try:
            cursor.execute('PRAGMA journal_mode=WAL')
            cursor.execute('PRAGMA synchronous=NORMAL')
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.execute('PRAGMA busy_timeout = 5000')
        except Exception:
            pass
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                session_id TEXT,
                ip_address TEXT,
                user_agent TEXT
            )
        ''')
        
        # Create activity log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                details TEXT,
                ip_address TEXT
            )
        ''')

        # Add indexes for better performance (after tables exist)
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_activity_log_user_id ON activity_log(user_id)')
        
        conn.commit()
        conn.close()
    
    def setup_logging(self):
        """Setup secure logging for family interactions"""
        log_dir = "family_data/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{log_dir}/family_app.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def encrypt_data(self, data):
        """Encrypt sensitive data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data"""
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return "[DECRYPTION_ERROR]"
    
    def _get_connection(self):
        """Get database connection with connection pooling"""
        import threading
        thread_id = threading.current_thread().ident
        
        if thread_id not in self._connection_pool:
            conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=10.0)
            # Configure connection for better concurrency
            try:
                conn.execute('PRAGMA journal_mode=WAL')
                conn.execute('PRAGMA synchronous=NORMAL')
                conn.execute('PRAGMA foreign_keys=ON')
                conn.execute('PRAGMA busy_timeout = 5000')
            except Exception:
                pass
            self._connection_pool[thread_id] = conn
        
        return self._connection_pool[thread_id]
    
    def save_conversation(self, user_id, user_message, ai_response, session_id=None, request_info=None):
        """Securely save conversation to database with validation"""
        if not user_id or not user_message or not ai_response:
            self.logger.error("Invalid conversation data provided")
            return False
            
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Encrypt sensitive conversation data
            encrypted_user_message = self.encrypt_data(user_message)
            encrypted_ai_response = self.encrypt_data(ai_response)
            
            ip_address = request_info.get('ip') if request_info else None
            user_agent = request_info.get('user_agent') if request_info else None
            
            cursor.execute('''
                INSERT INTO conversations 
                (user_id, user_message, ai_response, session_id, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, encrypted_user_message, encrypted_ai_response, session_id, ip_address, user_agent))
            
            conn.commit()
            
            self.logger.info(f"Conversation saved for user: {user_id}")
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"Database error saving conversation: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error saving conversation: {e}")
            return False
    
    def log_activity(self, user_id, activity_type, details=None, request_info=None):
        """Log user activity securely"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            ip_address = request_info.get('ip') if request_info else None
            encrypted_details = self.encrypt_data(details) if details else None
            
            cursor.execute('''
                INSERT INTO activity_log (user_id, activity_type, details, ip_address)
                VALUES (?, ?, ?, ?)
            ''', (user_id, activity_type, encrypted_details, ip_address))
            
            conn.commit()
            
            self.logger.info(f"Activity logged: {activity_type} for user: {user_id}")
            
        except Exception as e:
            self.logger.error(f"Error logging activity: {e}")
    
    def get_user_conversations(self, user_id, limit=50):
        """Get user's conversation history (decrypted)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, user_message, ai_response 
                FROM conversations 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (user_id, limit))
            
            conversations = []
            for row in cursor.fetchall():
                timestamp, encrypted_user_msg, encrypted_ai_resp = row
                conversations.append({
                    'timestamp': timestamp,
                    'user_message': self.decrypt_data(encrypted_user_msg),
                    'ai_response': self.decrypt_data(encrypted_ai_resp)
                })
            
            conn.close()
            return conversations
            
        except Exception as e:
            self.logger.error(f"Error retrieving conversations: {e}")
            return []

# Initialize secure data manager
secure_data = SecureDataManager()

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    """Redirect to login or family chat"""
    if 'username' in session:
        return redirect(url_for('family_chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Family member login"""
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form or {}
        username = str(data.get('username', '')).lower()
        password = str(data.get('password', ''))
        
        # Hash the provided password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Check credentials
        if username in FAMILY_USERS and FAMILY_USERS[username]['password'] == password_hash:
            session['username'] = username
            session['display_name'] = FAMILY_USERS[username]['display_name']
            session['role'] = FAMILY_USERS[username]['role']
            session['avatar'] = FAMILY_USERS[username]['avatar']
            session['session_id'] = hashlib.md5(f"{username}_{datetime.datetime.now()}".encode()).hexdigest()[:16]
            
            # Log successful login
            secure_data.log_activity(
                user_id=username,
                activity_type="login_success",
                details=f"Login successful for {FAMILY_USERS[username]['display_name']}",
                request_info={'ip': request.remote_addr, 'user_agent': request.headers.get('User-Agent', '')}
            )
            
            return jsonify({
                'success': True,
                'message': f'Welcome back, {FAMILY_USERS[username]["display_name"]}!',
                'redirect': '/chat'
            })
        else:
            # Log failed login attempt
            secure_data.log_activity(
                user_id=username if username else "unknown",
                activity_type="login_failed",
                details=f"Failed login attempt for username: {username}",
                request_info={'ip': request.remote_addr, 'user_agent': request.headers.get('User-Agent', '')}
            )
            
            return jsonify({
                'success': False,
                'message': 'Invalid username or password. Please try again.'
            }), 401
    
    return render_template('family_login.html')

@app.route('/logout')
def logout():
    """Logout current user"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/chat')
@login_required
def family_chat():
    """Main family chat interface"""
    return render_template('family_chat_app.html', 
                         user=session)

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """Handle chat messages with AI - Securely logged"""
    try:
        data = request.get_json(silent=True) or {}
        message = data.get('message', '').strip()
        
        # Input validation
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        if len(message) > 1000:
            return jsonify({'error': 'Message too long (max 1000 characters)'}), 400
        
        # Get AI response
        username = session['username']
        response = ai_chat_agent.chat_with_family_member(username, message)
        
        # Secure logging of conversation
        request_info = {
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', '')
        }
        
        # Save conversation securely
        secure_data.save_conversation(
            user_id=username,
            user_message=message,
            ai_response=response,
            session_id=session.get('session_id'),
            request_info=request_info
        )
        
        # Log activity
        secure_data.log_activity(
            user_id=username,
            activity_type="chat_message",
            details=f"Message length: {len(message)} chars",
            request_info=request_info
        )
        
        return jsonify({
            'user_message': message,
            'ai_response': response,
            'timestamp': datetime.datetime.now().strftime("%H:%M"),
            'user': session['display_name'],
            'avatar': session['avatar']
        })
        
    except ValueError as e:
        # Handle validation errors
        return jsonify({
            'error': 'Invalid input data',
            'ai_response': f"I didn't understand that, {session.get('display_name', 'there')}. Could you please rephrase?"
        }), 400
    except Exception as e:
        # Log error securely
        secure_data.log_activity(
            user_id=session.get('username', 'unknown'),
            activity_type="chat_error",
            details=f"Error: {str(e)}",
            request_info={'ip': request.remote_addr}
        )
        
        return jsonify({
            'error': 'Internal server error',
            'ai_response': f"I'm experiencing technical difficulties, {session.get('display_name', 'there')}, but I'm still here for you!"
        }), 500

@app.route('/api/voice-to-text', methods=['POST'])
@login_required  
def voice_to_text():
    """Process speech-to-text from browser"""
    try:
        data = request.get_json(silent=True) or {}
        speech_text = data.get('text', '')
        
        if not speech_text:
            return jsonify({
                'success': False,
                'error': 'No speech text provided'
            }), 400
        
        # Process the speech result
        result = voice_handler.process_browser_speech_result(speech_text)
        
        return jsonify({
            'success': result['success'],
            'text': result['text'],
            'confidence': result.get('confidence', 0.0),
            'source': result.get('source', 'browser')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/text-to-voice', methods=['POST'])
@login_required
def text_to_voice():
    """Convert text response to voice"""
    try:
        data = request.get_json(silent=True) or {}
        text = data.get('text', '')
        family_member = session.get('username', 'default')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        # Create audio file
        audio_path = voice_handler.create_audio_file(text, family_member)
        
        if audio_path:
            # Move to static directory for serving
            static_audio_dir = "static/audio"
            os.makedirs(static_audio_dir, exist_ok=True)
            
            audio_filename = f"response_{family_member}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            static_audio_path = os.path.join(static_audio_dir, audio_filename)
            
            # Copy file to static directory
            import shutil
            shutil.move(audio_path, static_audio_path)
            
            return jsonify({
                'success': True,
                'audio_url': f"/static/audio/{audio_filename}",
                'message': 'Voice synthesis complete'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate audio'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/voice-capabilities')
@login_required
def api_voice_capabilities():
    """Get voice system capabilities"""
    try:
        capabilities = voice_handler.get_voice_capabilities()
        return jsonify({
            'success': True,
            'capabilities': capabilities
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/family-info')
@login_required
def api_family_info():
    """Get current user's family information"""
    username = session['username']
    context = ai_chat_agent.memory_agent.get_member_context(username)
    is_admin = session.get('role') == 'admin'
    
    response_data = {
        'user': session,
        'context': context,
        'family_members': len(FAMILY_USERS),
        'ai_status': ai_chat_agent.test_ai_connection(),
        'voice_available': True,
        'is_admin': is_admin
    }
    
    # Admin-only information
    if is_admin:
        response_data['all_family_members'] = {
            username: {
                'display_name': user['display_name'],
                'role': user['role'],
                'avatar': user['avatar']
            } for username, user in FAMILY_USERS.items()
        }
    
    return jsonify(response_data)

@app.route('/api/conversation-starter')
@login_required
def api_conversation_starter():
    """Get a conversation starter from AI"""
    try:
        username = session['username']
        starter = ai_chat_agent.start_conversation(username)
        
        return jsonify({
            'starter': starter,
            'timestamp': datetime.datetime.now().strftime("%H:%M")
        })
    except Exception as e:
        return jsonify({
            'starter': f"Hello {session['display_name']}! How are you today?",
            'error': str(e)
        })

@app.route('/health')
def health():
    """Health check for the app"""
    return jsonify({
        'status': 'healthy',
        'ai_connected': ai_chat_agent.test_ai_connection(),
        'active_users': len([k for k in session.keys() if k == 'username']),
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 70)
    print("AdinavAI Complete Family App Starting...")
    print("=" * 70)
    
    # Test AI connection
    print("Testing AI connection...")
    if ai_chat_agent.test_ai_connection():
        print("AI model (GPT-OSS 20B) is ready!")
    else:
        print("AI model not ready yet. Basic features available.")
    
    print("\nFamily Login Credentials:")
    print("- Family members can login with their configured credentials")
    print("- Contact admin for login information if needed")
    
    print("\nFeatures Available:")
    print("- Family member login system")
    print("- Mobile-responsive design")
    print("- AI-powered conversations")
    print("- Voice input (READY - click microphone)")
    print("- Voice output (READY - automatic speech)")
    
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 8080))
    
    print("\nAccess your family app at:")
    print(f"   http://localhost:{port}")
    print(f"   http://192.168.1.156:{port} (for mobile devices)")
    print("=" * 70)
    
    try:
        print(f"\\nStarting server on http://localhost:{port}")
        print(f"Mobile access: http://192.168.1.156:{port}")
        app.run(debug=debug_mode, host='0.0.0.0', port=port, threaded=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {port} is busy, trying port {port + 1}")
            app.run(debug=debug_mode, host='0.0.0.0', port=port + 1, threaded=True)
        else:
            raise e