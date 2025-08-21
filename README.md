# AdinavAI Family System

A family-centric AI assistant system with voice capabilities, secure storage, and personalized interactions.

## 🚀 Quick Start

### Option 1: One-Click Startup (Windows)
```bash
# Double-click this file or run from command line:
start_adinav.bat
```

### Option 2: Python Startup Script
```bash
python start_adinav.py
```

### Option 3: Manual Startup
```bash
# 1. Start Ollama (if not already running)
ollama serve

# 2. Start the application
python family_app.py
```

## 📋 Prerequisites

### Required Software
- **Python 3.8+** - [Download here](https://python.org)
- **Ollama** - [Download here](https://ollama.ai)

### Required Models
```bash
# Install the AI model
ollama pull gpt-oss:20b
```

### Python Dependencies
```bash
pip install -r requirements.txt
```

## 🏠 Family Members

| Username | Password | Role | Avatar |
|----------|----------|------|--------|
| santosh | santosh2025 | Admin | 👨‍💼 |
| maryne | maryne2025 | Mother | 👩‍💼 |
| aditya | aditya2025 | Son | 👦 |
| avinav | avinav2025 | Son | 👦 |
| sushma | sushma2025 | Sister | 👩‍🦰 |
| meghna | meghna2025 | Niece | 👧 |

## 🌐 Access

Once started, access the application at:
- **Local**: http://localhost:8080
- **Mobile**: http://192.168.1.156:8080

## 🔧 Features

### ✅ Working Features
- **AI Chat**: Powered by gpt-oss:20b model
- **Voice Input**: Speech-to-text via browser API
- **Voice Output**: Text-to-speech with auto-speak
- **Family Authentication**: Secure login for each member
- **Conversation Memory**: Encrypted storage of chat history
- **Mobile Responsive**: Works on phones and tablets
- **Real-time Chat**: Instant messaging interface

### 🎯 Voice Commands
- Click the microphone button to speak
- Toggle auto-speak for AI responses
- Test voice functionality with the Test button
- Run audio diagnostics for troubleshooting

## 🛠️ Troubleshooting

### Common Issues

#### 1. "Ollama not running" Error
```bash
# Start Ollama manually
ollama serve

# Or check if it's already running
curl http://localhost:11434/api/tags
```

#### 2. "Model not found" Error
```bash
# Install the required model
ollama pull gpt-oss:20b

# Check available models
ollama list
```

#### 3. "Port already in use" Error
The system automatically finds free ports (8080, 5000, 3000, etc.)

#### 4. Voice not working
- Check browser permissions for microphone
- Try the "Debug" button for diagnostics
- Ensure HTTPS or localhost (required for voice)

### System Health Check
```bash
python system_check.py
```

## 📁 Project Structure

```
AdinavAI_Family/
├── agents/                    # AI agent modules
│   ├── ai_powered_chat_agent.py
│   ├── family_memory_agent.py
│   └── voice_handler.py
├── family_data/              # Secure data storage
│   ├── secure_conversations.db
│   ├── family_members.json
│   └── logs/
├── templates/                # Web interface
│   ├── family_chat_app.html
│   └── family_login.html
├── start_adinav.py          # Smart startup script
├── start_adinav.bat         # Windows batch file
├── family_app.py            # Main application
├── system_check.py          # Health diagnostics
└── requirements.txt         # Python dependencies
```

## 🔒 Security Features

- **Encrypted Storage**: All conversations encrypted with AES-256
- **Secure Authentication**: SHA-256 password hashing
- **Session Management**: Secure session handling
- **Input Validation**: Protection against malicious input
- **Activity Logging**: Complete audit trail

## 🎨 Customization

### Adding Family Members
Edit `family_app.py` and add to `FAMILY_USERS`:
```python
"newmember": {
    "password": hashlib.sha256("password123".encode()).hexdigest(),
    "display_name": "New Member",
    "role": "member",
    "avatar": "👤"
}
```

### Changing AI Model
Edit `agents/ai_powered_chat_agent.py`:
```python
self.model_name = "your-model-name"
```

## 📞 Support

If you encounter issues:
1. Run `python system_check.py` for diagnostics
2. Check the logs in `family_data/logs/`
3. Ensure Ollama is running: `ollama serve`
4. Verify model is installed: `ollama list`

## 🚀 Future Enhancements

- Multi-agent architecture (coding, financial, health agents)
- Vector database for semantic memory
- Redis caching for performance
- Advanced voice processing
- Mobile app development
- Open-source community features

---

**Created with ❤️ by Santosh Gupta for the Gupta Family**
