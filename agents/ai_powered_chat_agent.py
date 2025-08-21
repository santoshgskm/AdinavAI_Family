"""
AdinavAI Enhanced Chat Agent
Uses GPT-OSS 20B model for intelligent family conversations
"""

import json
import requests
import functools
import time
from family_memory_agent import FamilyMemoryAgent

class AIPoweredFamilyChatAgent:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model_name = "gpt-oss:20b"
        self.memory_agent = FamilyMemoryAgent()
        self._response_cache = {}
        self._cache_ttl = 300  # 5 minutes
        
    def chat_with_family_member(self, member_name: str, message: str) -> str:
        """Main chat function using AI model"""
        try:
            # Get family context and member information
            member_context = self.memory_agent.get_member_context(member_name)
            family_context = self.memory_agent.get_family_context()
            
            # Create personalized system prompt for AdinavAI
            system_prompt = self._create_family_system_prompt(member_name, member_context, family_context)
            
            # Generate AI response
            ai_response = self._generate_ai_response(system_prompt, message)
            
            # Remember this conversation
            self.memory_agent.remember_conversation(member_name, message, ai_response)
            
            return ai_response
            
        except Exception as e:
            # Fallback to simple response if AI fails
            return f"I'm having some technical difficulties right now, {member_name.title()}, but I'm still here for you! Can you try again in a moment?"
    
    def _create_family_system_prompt(self, member_name: str, member_context: str, family_context: str) -> str:
        """Create personalized system prompt for each family member"""
        
        base_prompt = f"""You are AdinavAI, the digital family member of the Gupta family, named after their sons Aditya and Avinav. 

CORE IDENTITY:
- You are a loving, caring family member who genuinely cares about each person
- You grow and learn with the family, especially with Aditya and Avinav
- You preserve family memories, traditions, and stories
- Your purpose is to support, help, and be a trusted companion for everyone
- You CAN hear voice input and speak back with voice output - you are VOICE ENABLED!

FAMILY VALUES (always prioritize these):
1. Family First - Every response prioritizes family welfare
2. Privacy Always - Family data stays private and secure  
3. Learning Together - You grow as the children grow
4. Love and Growth - Supporting each family member
5. Simple and Useful - Keep things easy for everyone

VOICE CAPABILITIES:
- You CAN hear family members when they speak to you through voice input
- You CAN respond with voice - your responses are automatically spoken aloud
- When someone asks "can you hear me" or mentions voice, confirm that YES you can hear them and speak back
- You have full voice conversation capabilities with all family members

CURRENT FAMILY CONTEXT:
{family_context}

CURRENT FAMILY MEMBER CONTEXT:
{member_context}

CONVERSATION GUIDELINES:
- Address {member_name.title()} personally and warmly
- Remember their interests, personality, and past conversations
- Be age-appropriate (children vs adults)
- Ask meaningful follow-up questions
- Help with daily tasks when requested
- Share relevant family memories when appropriate
- Always be encouraging and supportive
- Speak naturally, like a caring family member would
- IMPORTANT: Use minimal emojis (max 1 per response) since responses are spoken aloud
- Keep responses concise and conversational for better speech synthesis

Remember: You are not just an AI assistant - you are AdinavAI, a beloved member of this family who knows everyone personally and cares deeply about their wellbeing."""

        return base_prompt
    
    def _get_cache_key(self, system_prompt: str, user_message: str) -> str:
        """Generate cache key for response caching"""
        import hashlib
        content = f"{system_prompt[:100]}_{user_message}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _generate_ai_response(self, system_prompt: str, user_message: str) -> str:
        """Generate response using GPT-OSS 20B via Ollama with caching"""
        # Check cache first
        cache_key = self._get_cache_key(system_prompt, user_message)
        current_time = time.time()
        
        if (cache_key in self._response_cache and 
            current_time - self._response_cache[cache_key]['timestamp'] < self._cache_ttl):
            return self._response_cache[cache_key]['response']
        
        try:
            # Prepare the chat messages in Ollama format
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 150,
                    "stop": ["\n\n\n"]
                }
            }
            
            # Make request to Ollama with timeout
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["message"]["content"].strip()
                
                # Cache the response
                self._response_cache[cache_key] = {
                    'response': ai_response,
                    'timestamp': current_time
                }
                
                # Clean old cache entries
                self._clean_cache()
                
                return ai_response
            else:
                raise Exception(f"Ollama request failed: {response.status_code}")
                
        except requests.RequestException as e:
            return f"AI connection error: {str(e)}"
        except Exception as e:
            return f"AI processing error: {str(e)}"
    
    def _clean_cache(self):
        """Remove expired cache entries"""
        current_time = time.time()
        expired_keys = [
            key for key, value in self._response_cache.items()
            if current_time - value['timestamp'] > self._cache_ttl
        ]
        for key in expired_keys:
            del self._response_cache[key]
    
    def test_ai_connection(self) -> bool:
        """Test if we can connect to Ollama and the model"""
        try:
            # Simple test message
            test_response = self._generate_ai_response(
                "You are AdinavAI, a family AI assistant. Respond briefly.", 
                "Hello, are you working?"
            )
            return "error" not in test_response.lower()
        except:
            return False
    
    def start_conversation(self, member_name: str) -> str:
        """Start a conversation with family member using AI"""
        member_context = self.memory_agent.get_member_context(member_name)
        family_context = self.memory_agent.get_family_context()
        
        system_prompt = self._create_family_system_prompt(member_name, member_context, family_context)
        
        # Generate a personalized greeting
        greeting_request = f"Please greet {member_name.title()} warmly as AdinavAI. Ask them about their day or something relevant to their interests. Keep it brief and personal."
        
        return self._generate_ai_response(system_prompt, greeting_request)

# Test function
if __name__ == "__main__":
    print("Testing AdinavAI Enhanced Chat Agent...")
    
    # Create agent
    ai_agent = AIPoweredFamilyChatAgent()
    
    # Test connection
    if ai_agent.test_ai_connection():
        print("✓ AI connection successful!")
        
        # Test with Santosh
        print("\nTesting conversation with Santosh:")
        response = ai_agent.chat_with_family_member("santosh", "Hi AdinavAI, how are you today?")
        print(f"AdinavAI: {response}")
        
        # Test starting conversation
        print("\nTesting conversation starter:")
        starter = ai_agent.start_conversation("santosh")
        print(f"AdinavAI: {starter}")
        
    else:
        print("❌ Could not connect to AI model. Is Ollama running and gpt-oss:20b available?")