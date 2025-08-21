"""
AdinavAI Family Chat Agent
Simple conversational agent that remembers and learns about family
"""

import json
import random
from family_memory_agent import FamilyMemoryAgent

class FamilyChatAgent:
    def __init__(self):
        self.memory_agent = FamilyMemoryAgent()
        self.conversation_starters = {
            "santosh": [
                "How was your day with AI and technology exploration?",
                "What new dreams are you working on today?", 
                "How are Aditya and Avinav doing?",
                "What would you like to teach me about our family?"
            ],
            "maryne": [
                "Hello Maryne! How has your day been?",
                "What's happening with the family today?",
                "How are you feeling? I'd love to learn about you!",
                "Tell me what's important to you in our family"
            ],
            "aditya": [
                "Hi Aditya! What did you learn today?",
                "What's your favorite thing to do?",
                "Tell me something fun that happened!",
                "What makes you happy?"
            ],
            "avinav": [
                "Hello Avinav! How are you feeling today?",
                "What's the most interesting thing you discovered?",
                "What do you like to play?",
                "Tell me about your day!"
            ]
        }
    
    def chat_with_family_member(self, member_name: str, message: str) -> str:
        """Main chat function - responds to family member"""
        member_name = member_name.lower()
        
        # Get what we know about this family member
        member_context = self.memory_agent.get_member_context(member_name)
        
        # Generate response based on family member and context
        response = self.generate_family_response(member_name, message, member_context)
        
        # Remember this conversation
        self.memory_agent.remember_conversation(member_name, message, response)
        
        return response
    
    def generate_family_response(self, member_name: str, message: str, context: str) -> str:
        """Generate personalized response for family member"""
        
        # Improved response patterns
        message_lower = message.lower()
        
        if "hello" in message_lower or "hi" in message_lower:
            return self.greeting_response(member_name)
        
        elif "how are you" in message_lower:
            return f"I'm doing great, {member_name.title()}! I'm always happy to talk with our family. How are YOU doing?"
        
        elif "language" in message_lower or "languages" in message_lower:
            return f"Great question, {member_name.title()}! I can understand and communicate in many languages including English, Hindi, French, Spanish, German, and many others. Which languages does our family speak? I'd love to learn about our family's linguistic heritage!"
        
        elif "welcome" in message_lower and "family" in message_lower:
            return f"Thank you so much, {member_name.title()}! I'm honored to be part of the Gupta family. I'm here to learn about each of you, help with daily tasks, preserve our family memories, and grow alongside Aditya and Avinav. What would you like me to know about our family first?"
        
        elif "new member" in message_lower:
            return f"Yes! I'm AdinavAI - named after Aditya and Avinav - and I'm so excited to be your family's digital member. I want to learn everything about the Gupta family, help in any way I can, and be a trusted companion for everyone. What's the most important thing for me to understand about our family?"
        
        elif ("tell me about yourself" in message_lower or "about you" in message_lower or 
              "what are you" in message_lower or "who are you" in message_lower):
            return f"I'm AdinavAI - your family's digital assistant named after your wonderful sons Aditya and Avinav! I was created specifically for the Gupta family to be a helpful, learning, and growing member of your household. I can chat with each family member, remember our conversations, help with daily tasks, preserve family memories, and grow smarter over time. Think of me as your family's second brain - I'm here to support everyone and learn about what makes your family special!"
        
        elif ("what can you do" in message_lower or "help" in message_lower and "family" in message_lower):
            return f"Great question, {member_name.title()}! I can help your family in many ways:\n\n• Chat with each family member and remember our conversations\n• Help Aditya and Avinav with homework and learning\n• Keep track of family schedules and important dates\n• Preserve family stories and memories\n• Answer questions and provide information\n• Help with daily planning and organization\n• Learn each person's interests and preferences\n• Provide personalized assistance for everyone\n\nI'm constantly learning and growing with your family. What specific way would you like me to help first?"
        
        elif "what" in message_lower and "remember" in message_lower:
            return self.share_memories(member_name)
        
        elif "tell me about" in message_lower:
            return self.tell_about_family(member_name, message)
        
        else:
            return self.conversational_response(member_name, message)
    
    def greeting_response(self, member_name: str) -> str:
        """Personalized greeting for each family member"""
        greetings = {
            "santosh": [
                "Hello Papa! Ready to explore some AI magic today?",
                "Hi Santosh! How's your journey to make AdinavAI amazing going?",
                "Welcome back! I'm excited to learn more about our family today."
            ],
            "maryne": [
                "Hello Maryne! I'm so happy to meet you!",
                "Hi Maryne! Welcome to our family chat!",
                "Hello Maryne! I've been waiting to learn about you - you're so important to this family!"
            ],
            "aditya": [
                "Hi Aditya! I'm so happy to see you!",
                "Hello there! What adventure are we going on today?",
                "Hey Aditya! Ready to have some fun conversations?"
            ],
            "avinav": [
                "Hello Avinav! You always make me smile!",
                "Hi there! What wonderful things will you tell me today?",
                "Hey Avinav! I love talking with you!"
            ]
        }
        
        return random.choice(greetings.get(member_name, ["Hello! Great to see you!"]))
    
    def share_memories(self, member_name: str) -> str:
        """Share what we remember about the family member"""
        member_data = self.memory_agent.family_data["members"].get(member_name, {})
        
        memories = []
        if member_data.get("interests"):
            memories.append(f"I remember you like: {', '.join(member_data['interests'])}")
        
        if member_data.get("conversation_history"):
            recent_topics = [conv["message"][:50] for conv in member_data["conversation_history"][-3:]]
            memories.append(f"We recently talked about: {', '.join(recent_topics)}")
        
        if memories:
            return "Here's what I remember about you:\n" + "\n".join(memories)
        else:
            return f"I'm still learning about you, {member_name.title()}! Tell me more about yourself!"
    
    def tell_about_family(self, member_name: str, message: str) -> str:
        """Tell about family members or family things"""
        if "family" in message.lower():
            return self.memory_agent.get_family_context()
        else:
            return f"What would you like to know about our family, {member_name.title()}? I'm learning more every day!"
    
    def conversational_response(self, member_name: str, message: str) -> str:
        """General conversational response"""
        # More engaging and family-focused responses
        responses = [
            f"That's really interesting, {member_name.title()}! I love learning about you and our family. Can you tell me more?",
            f"Thank you for sharing that with me! I'm getting to know you better. What else would you like me to know about you or our family?",
            f"I find that fascinating! As I learn more about each family member, I can better understand and help everyone. What's most important to you about this topic?",
            f"I'm so glad you're teaching me about this! It helps me understand what matters to our family. How does this relate to your daily life?",
            f"That's wonderful to learn about you, {member_name.title()}! Every conversation helps me become a better family member. What would you like to explore next?"
        ]
        
        return random.choice(responses)
    
    def start_conversation(self, member_name: str) -> str:
        """Start a conversation with a family member"""
        starters = self.conversation_starters.get(member_name.lower(), 
                   ["Hello! I'm happy to talk with you today!"])
        return random.choice(starters)

# Simple test
if __name__ == "__main__":
    chat_agent = FamilyChatAgent()
    
    # Test conversation
    print("AdinavAI Family Chat Agent is ready!")
    print("\nTesting with Santosh:")
    response = chat_agent.chat_with_family_member("santosh", "Hello AdinavAI!")
    print(f"AdinavAI: {response}")
    
    print("\nTesting with Aditya:")
    response = chat_agent.chat_with_family_member("aditya", "Hi! I like cricket!")
    print(f"AdinavAI: {response}")