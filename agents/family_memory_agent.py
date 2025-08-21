"""
AdinavAI Family Memory Agent
Remembers everything about our family - conversations, preferences, memories
"""

import json
import datetime
import os
from typing import Dict, List, Any

class FamilyMemoryAgent:
    def __init__(self, data_path=None):
        if data_path is None:
            # Get the directory where the script is located, then go up one level
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(current_dir, "family_data")
        self.data_path = data_path
        self.family_file = os.path.join(data_path, "family_members.json")
        self.conversations_file = os.path.join(data_path, "daily_conversations.json")
        self.family_data = self.load_family_data()
    
    def load_family_data(self) -> Dict:
        """Load family data from JSON file"""
        # Ensure directory exists
        os.makedirs(self.data_path, exist_ok=True)
        
        try:
            if os.path.exists(self.family_file):
                with open(self.family_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.create_initial_family_data()
        except (FileNotFoundError, json.JSONDecodeError):
            return self.create_initial_family_data()
    
    def save_family_data(self):
        """Save family data to JSON file"""
        with open(self.family_file, 'w', encoding='utf-8') as f:
            json.dump(self.family_data, f, indent=2, ensure_ascii=False)
    
    def remember_conversation(self, member_name: str, message: str, ai_response: str):
        """Remember a conversation with a family member"""
        timestamp = datetime.datetime.now().isoformat()
        
        conversation_entry = {
            "timestamp": timestamp,
            "member": member_name.lower(),
            "message": message,
            "ai_response": ai_response,
            "day": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        
        # Add to member's conversation history
        if member_name.lower() in self.family_data["members"]:
            self.family_data["members"][member_name.lower()]["conversation_history"].append(conversation_entry)
        
        # Save daily conversations
        self.save_daily_conversation(conversation_entry)
        self.save_family_data()
        
        # Learn from the conversation
        self.learn_from_conversation(member_name.lower(), message)
    
    def save_daily_conversation(self, conversation_entry: Dict):
        """Save conversation to daily log"""
        try:
            with open(self.conversations_file, 'r', encoding='utf-8') as f:
                daily_conversations = json.load(f)
        except FileNotFoundError:
            daily_conversations = []
        
        daily_conversations.append(conversation_entry)
        
        with open(self.conversations_file, 'w', encoding='utf-8') as f:
            json.dump(daily_conversations, f, indent=2, ensure_ascii=False)
    
    def learn_from_conversation(self, member_name: str, message: str):
        """Learn about family member from their message"""
        message_lower = message.lower()
        
        # Simple learning patterns - we'll make this smarter over time
        if "like" in message_lower or "love" in message_lower:
            # Extract interests
            self.extract_interests(member_name, message)
        
        if "feel" in message_lower or "think" in message_lower:
            # Extract personality traits
            self.extract_personality_traits(member_name, message)
        
        # Always save what we learn
        self.save_family_data()
    
    def extract_interests(self, member_name: str, message: str):
        """Extract interests from conversation"""
        interests = self.family_data["members"][member_name].get("interests", [])
        
        # Simple keyword extraction - we'll improve this
        keywords = ["football", "cricket", "reading", "games", "music", "art", "science", "math"]
        for keyword in keywords:
            if keyword in message.lower() and keyword not in interests:
                interests.append(keyword)
        
        self.family_data["members"][member_name]["interests"] = interests
    
    def extract_personality_traits(self, member_name: str, message: str):
        """Extract personality traits from conversation"""
        # This will become more sophisticated with AI
        current_personality = self.family_data["members"][member_name].get("personality", "")
        
        # For now, just append new observations
        if len(message) > 20:  # Meaningful message
            self.family_data["members"][member_name]["personality"] = current_personality + f" | {datetime.date.today()}: observed from conversation"
    
    def get_member_context(self, member_name: str) -> str:
        """Get everything we know about a family member"""
        member = self.family_data["members"].get(member_name.lower(), {})
        
        context = f"Family Member: {member.get('name', member_name)}\n"
        context += f"Role: {member.get('role', 'unknown')}\n"
        context += f"Interests: {', '.join(member.get('interests', []))}\n"
        context += f"Personality: {member.get('personality', 'learning...')}\n"
        
        # Recent conversations
        recent_conversations = member.get("conversation_history", [])[-5:]  # Last 5 conversations
        if recent_conversations:
            context += "\nRecent conversations:\n"
            for conv in recent_conversations:
                context += f"- {conv['timestamp'][:10]}: {conv['message'][:100]}...\n"
        
        return context
    
    def get_family_context(self) -> str:
        """Get overall family context"""
        family_info = self.family_data["family"]
        context = f"Family: {family_info['name']}\n"
        context += f"Family Values: {', '.join(family_info['values'])}\n"
        context += f"Members: {', '.join([member['name'] for member in self.family_data['members'].values()])}\n"
        
        return context
    
    def create_initial_family_data(self) -> Dict:
        """Create initial family data structure"""
        initial_data = {
            "family": {
                "name": "Gupta Family",
                "values": ["Family First", "Privacy Always", "Learning Together", "Love and Growth", "Simple and Useful"]
            },
            "members": {
                "santosh": {
                    "name": "Santosh Gupta",
                    "role": "admin",
                    "interests": [],
                    "personality": "Family creator and administrator",
                    "conversation_history": []
                },
                "maryne": {
                    "name": "Maryne Gupta",
                    "role": "mother",
                    "interests": [],
                    "personality": "Caring mother",
                    "conversation_history": []
                },
                "aditya": {
                    "name": "Aditya Gupta",
                    "role": "son",
                    "interests": [],
                    "personality": "Young family member",
                    "conversation_history": []
                },
                "avinav": {
                    "name": "Avinav Gupta",
                    "role": "son",
                    "interests": [],
                    "personality": "Young family member",
                    "conversation_history": []
                },
                "sushma": {
                    "name": "Sushma Potlapally",
                    "role": "sister",
                    "interests": [],
                    "personality": "Visiting from Germany",
                    "conversation_history": []
                },
                "meghna": {
                    "name": "Meghna Potlapally",
                    "role": "niece",
                    "interests": [],
                    "personality": "Sushma's daughter",
                    "conversation_history": []
                }
            }
        }
        
        # Save the initial data
        self.save_family_data_dict(initial_data)
        return initial_data
    
    def save_family_data_dict(self, data: Dict):
        """Save family data dictionary to file"""
        os.makedirs(self.data_path, exist_ok=True)
        with open(self.family_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

# Simple test
if __name__ == "__main__":
    agent = FamilyMemoryAgent()
    print("AdinavAI Family Memory Agent is ready!")
    print(agent.get_family_context())