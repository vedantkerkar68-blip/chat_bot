#!/usr/bin/env python3
"""
Test script for Text-to-Speech functionality
"""
from voice_utils import VoiceManager

def test_tts():
    """Test the text-to-speech functionality."""
    print("Testing Text-to-Speech...")
    
    try:
        # Initialize voice manager
        voice_manager = VoiceManager()
        
        # Test message
        test_message = "Hello! This is a test of the text-to-speech system. I can read AI responses aloud."
        
        print(f"\nSpeaking: {test_message}")
        voice_manager.speak(test_message, blocking=True)
        
        print("\n✅ Text-to-Speech test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Text-to-Speech test failed: {e}")
        return False

if __name__ == "__main__":
    test_tts()
