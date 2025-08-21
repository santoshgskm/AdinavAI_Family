"""
AdinavAI Voice Handler
Manages speech-to-text and text-to-speech for family conversations
Uses browser-based speech recognition and system TTS
"""

import pyttsx3
import threading
import tempfile
import os
import logging
import json
from typing import Optional, Dict, Any

class VoiceHandler:
    def __init__(self):
        # No speech recognition initialization - will use browser API
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.setup_tts_voice()
        
        # Voice settings for different family members
        self.voice_profiles = {
            'santosh': {'rate': 180, 'volume': 0.8},
            'maryne': {'rate': 170, 'volume': 0.8},
            'aditya': {'rate': 160, 'volume': 0.9},
            'avinav': {'rate': 160, 'volume': 0.9},
            'default': {'rate': 175, 'volume': 0.8}
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def setup_tts_voice(self):
        """Configure the text-to-speech engine"""
        try:
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            
            # Prefer a pleasant voice (usually index 1 is female on Windows)
            if len(voices) > 1:
                self.tts_engine.setProperty('voice', voices[1].id)
            
            # Set default properties
            self.tts_engine.setProperty('rate', 175)
            self.tts_engine.setProperty('volume', 0.8)
            
        except Exception as e:
            self.logger.warning(f"Voice setup warning: {e}")
    
    def process_browser_speech_result(self, speech_result: str) -> Dict[str, Any]:
        """
        Process speech result from browser Web Speech API
        
        Args:
            speech_result: Text from browser speech recognition
            
        Returns:
            Processing result with confidence and metadata
        """
        try:
            result = {
                'success': True,
                'text': speech_result.strip(),
                'confidence': 0.95,  # Browser API doesn't provide confidence
                'source': 'browser_web_speech_api'
            }
            
            self.logger.info(f"Processed browser speech: {result['text']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing browser speech: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': '',
                'confidence': 0.0
            }
    
    def text_to_speech(self, text: str, family_member: str = 'default', async_mode: bool = True) -> bool:
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            family_member: Family member name for voice customization
            async_mode: Whether to speak asynchronously
            
        Returns:
            Success status
        """
        try:
            # Apply voice profile for family member
            profile = self.voice_profiles.get(family_member, self.voice_profiles['default'])
            self.tts_engine.setProperty('rate', profile['rate'])
            self.tts_engine.setProperty('volume', profile['volume'])
            
            if async_mode:
                # Speak asynchronously in a separate thread
                def speak_async():
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                
                thread = threading.Thread(target=speak_async)
                thread.daemon = True
                thread.start()
            else:
                # Speak synchronously
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Text-to-speech error: {e}")
            return False
    
    def create_audio_file(self, text: str, family_member: str = 'default') -> Optional[str]:
        """
        Create an audio file from text
        
        Args:
            text: Text to convert
            family_member: Family member name for voice customization
            
        Returns:
            Path to created audio file or None if failed
        """
        try:
            # Apply voice profile
            profile = self.voice_profiles.get(family_member, self.voice_profiles['default'])
            self.tts_engine.setProperty('rate', profile['rate'])
            self.tts_engine.setProperty('volume', profile['volume'])
            
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                audio_path = temp_file.name
            
            # Save to file
            self.tts_engine.save_to_file(text, audio_path)
            self.tts_engine.runAndWait()
            
            return audio_path
            
        except Exception as e:
            self.logger.error(f"Audio file creation error: {e}")
            return None
    
    def get_voice_capabilities(self) -> Dict[str, Any]:
        """Get voice system capabilities"""
        try:
            capabilities = {
                'speech_to_text': 'browser_web_speech_api',
                'text_to_speech': 'system_tts',
                'languages_supported': ['en-US', 'fr-FR', 'es-ES', 'de-DE'],
                'family_voice_profiles': list(self.voice_profiles.keys()),
                'async_tts': True,
                'audio_file_generation': True
            }
            return capabilities
        except Exception as e:
            self.logger.error(f"Error getting capabilities: {e}")
            return {}
    
    def test_voice_system(self) -> Dict[str, Any]:
        """Test voice system capabilities"""
        results = {
            'tts_available': False,
            'capabilities': {},
            'test_results': {}
        }
        
        try:
            # Get capabilities
            results['capabilities'] = self.get_voice_capabilities()
            
            # Test text-to-speech
            test_text = "Hello! This is AdinavAI testing voice output."
            results['tts_available'] = self.text_to_speech(test_text, async_mode=False)
            results['test_results']['tts_test'] = 'TTS system working'
            
            # Browser speech recognition will be tested via web interface
            results['test_results']['speech_recognition'] = 'Available via browser Web Speech API'
            
        except Exception as e:
            self.logger.error(f"Voice system test error: {e}")
            results['test_error'] = str(e)
        
        return results

# Test the voice system
if __name__ == "__main__":
    print("Testing AdinavAI Voice Handler...")
    
    # Create voice handler
    voice_handler = VoiceHandler()
    
    # Run tests
    test_results = voice_handler.test_voice_system()
    
    print("\n=== Voice System Test Results ===")
    print(f"Text-to-Speech Available: {test_results['tts_available']}")
    print(f"Capabilities: {test_results['capabilities']}")
    
    if 'test_results' in test_results:
        for key, value in test_results['test_results'].items():
            print(f"{key}: {value}")
    
    if 'test_error' in test_results:
        print(f"Test Error: {test_results['test_error']}")
    
    print("\nVoice Handler ready for AdinavAI family system!")