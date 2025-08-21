# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## AdinavAI Family System

AdinavAI is a personal family AI assistant created by Santosh Gupta, named after his sons Aditya and Avinav. It's a complete voice-enabled conversational AI system designed specifically for the Gupta family members.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the main family application
python family_app.py

# Access at http://localhost:5000
```

## Core Architecture

### Main Application (`family_app.py`)
- **Flask web server** serving the complete family interface
- **Secure authentication system** with individual family member credentials
- **Encrypted data storage** using Fernet encryption for all conversations
- **Voice integration** with speech-to-text and text-to-speech capabilities
- **Admin role system** - only Santosh has admin access, others have standard family access

### AI Agent System (`agents/`)
- **`ai_powered_chat_agent.py`**: Main AI interface using Ollama with GPT-OSS 20B model
- **`family_memory_agent.py`**: Persistent memory system storing family conversations, preferences, and personality observations
- **`voice_handler.py`**: Voice processing with browser Web Speech API integration and system TTS

### Data Architecture
- **SQLite database**: Encrypted conversation storage (`family_data/secure_conversations.db`)
- **JSON files**: Family member profiles and memories (`family_data/family_members.json`)
- **Encryption keys**: Auto-generated Fernet keys for data security (`family_data/encryption.key`)

## Family Members

Current family members with individual credentials:
- **santosh** (Admin): Creator and system administrator
- **maryne** (Mother): Santosh's wife
- **aditya** (Son): Family member
- **avinav** (Son): Family member  
- **sushma** (Sister): Visiting from Germany
- **meghna** (Niece): Sushma's daughter

## AI Model Integration

### Ollama Configuration
- **Model**: `gpt-oss:20b` running on `http://localhost:11434`
- **Features**: Voice-aware prompts, family context integration, multilingual support
- **Fallback**: Graceful degradation when AI model is unavailable

### Voice System
- **Input**: Browser Web Speech API for real-time voice recognition
- **Output**: System TTS with language detection (English, French, Spanish, German)
- **Quality**: Automatic voice selection with fallback for better user experience

## Key Features

### Secure Family Authentication
- SHA-256 hashed passwords
- Session-based authentication with role-based access
- Individual login credentials for each family member

### Conversation Memory System
- **Long-term memory**: Persistent storage of all family conversations
- **Context awareness**: AI remembers personality traits, preferences, and family dynamics
- **Daily conversation logs**: Timestamped interaction history
- **Personality learning**: System adapts to each family member's communication style

### Voice Capabilities
- **Real-time speech recognition**: Click-to-talk interface
- **Automatic speech synthesis**: AI responses spoken aloud
- **Language detection**: Automatic language switching for French/Spanish/German
- **Family-specific voice profiles**: Customized speech settings per family member

## Development Commands

```bash
# Test AI connection
python -c "import sys; sys.path.append('agents'); from ai_powered_chat_agent import AIPoweredFamilyChatAgent; agent = AIPoweredFamilyChatAgent(); print('AI Connected:', agent.test_ai_connection())"

# Test voice system
python agents/voice_handler.py

# Start alternative interfaces
python start_family_ai.py  # Simple launcher
python web_interface/app.py  # Alternative web interface
```

## Technical Dependencies

### Required Services
- **Ollama**: Must be running with `gpt-oss:20b` model downloaded
- **Browser with Web Speech API**: Chrome, Edge, or compatible browser for voice features

### Python Dependencies
- **Flask**: Web application framework
- **cryptography**: Data encryption for family privacy
- **requests**: Ollama API communication
- **speechrecognition + pyttsx3**: Voice processing (optional fallback)

## Data Privacy & Security

### Encryption
- All family conversations encrypted using Fernet symmetric encryption
- Automatic encryption key generation and management
- Secure password hashing with SHA-256

### Local-First Architecture
- All data stored locally on family computer
- No external API calls for family data
- Ollama runs locally for AI processing

## Code Organization Principles

### Agent Pattern
- Each AI capability encapsulated in separate agent classes
- Clear separation between memory, chat, and voice functionality
- Modular design allows independent feature development

### Family-Centric Design
- All prompts and responses tailored to family context
- Personality-aware interactions based on stored family member data
- Role-based access control respecting family hierarchy

### Voice-First Interface
- Frontend designed for both text and voice interaction
- Automatic language detection and appropriate voice synthesis
- Fallback mechanisms ensure functionality across different environments

## Important Implementation Notes

- **Family data paths**: All data stored in `family_data/` directory with automatic creation
- **Session management**: Flask sessions track individual family member authentication
- **Error handling**: Graceful fallbacks when AI or voice services unavailable
- **Mobile responsive**: Interface optimized for family use on various devices
- **Admin features**: Santosh has additional access to family member management and system logs