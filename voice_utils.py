import speech_recognition as sr
import pyttsx3
import threading
import queue
from typing import Optional, Callable
import time
import os

class VoiceManager:
    def __init__(self):
        """Initialize voice manager with speech recognition and text-to-speech."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech engine
        try:
            self.tts_engine = pyttsx3.init()
            self.setup_tts()
        except Exception as e:
            print(f"Error initializing TTS engine: {e}")
            self.tts_engine = None
        
        # Voice recognition settings
        self.energy_threshold = 4000
        self.dynamic_energy_threshold = True
        self.pause_threshold = 0.8
        self.phrase_threshold = 0.3
        
        self.setup_microphone()
        
        # Threading
        self.is_listening = False
        self.is_speaking = False
        self.voice_queue = queue.Queue()
    
    def setup_microphone(self):
        """Configure microphone settings."""
        try:
            with self.microphone as source:
                print("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.recognizer.energy_threshold = self.energy_threshold
            self.recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold
            self.recognizer.pause_threshold = self.pause_threshold
            self.recognizer.phrase_threshold = self.phrase_threshold
            
            print("Microphone setup completed.")
            
        except Exception as e:
            print(f"Error setting up microphone: {e}")
    
    def setup_tts(self):
        """Configure text-to-speech settings."""
        if not self.tts_engine:
            return
        
        try:
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            
            # Set voice (prefer female voice if available)
            if voices:
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 200)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
            
            print("Text-to-speech setup completed.")
            
        except Exception as e:
            print(f"Error setting up TTS: {e}")
    
    def listen_once(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for a single voice input.
        
        Args:
            timeout (int): Seconds to wait for speech to begin
            phrase_time_limit (int): Maximum seconds to record phrase
            
        Returns:
            str: Recognized text or None if recognition failed
        """
        try:
            print("Listening... Speak now!")
            
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            print("Processing speech...")
            
            # Recognize speech using Google's service
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return None
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None
    
    def listen_continuous(self, callback: Callable[[str], None], stop_event: threading.Event):
        """
        Listen continuously for voice input.
        
        Args:
            callback (function): Function to call with recognized text
            stop_event (threading.Event): Event to stop listening
        """
        self.is_listening = True
        print("Starting continuous listening...")
        
        def listen_in_background():
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            while not stop_event.is_set() and self.is_listening:
                try:
                    with self.microphone as source:
                        # Listen for audio with shorter timeout for continuous mode
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio)
                    if text.strip():
                        callback(text)
                        
                except sr.WaitTimeoutError:
                    continue  # Normal timeout, continue listening
                except sr.UnknownValueError:
                    continue  # Couldn't understand, continue listening
                except sr.RequestError as e:
                    print(f"Speech recognition error: {e}")
                    break
                except Exception as e:
                    print(f"Error in continuous listening: {e}")
                    break
        
        # Start listening in background thread
        listen_thread = threading.Thread(target=listen_in_background, daemon=True)
        listen_thread.start()
        
        return listen_thread
    
    def speak(self, text: str, blocking: bool = True):
        """
        Convert text to speech.
        
        Args:
            text (str): Text to speak
            blocking (bool): Wait for speech to complete before returning
        """
        if not self.tts_engine or not text.strip():
            return
        
        def speak_text():
            try:
                self.is_speaking = True
                print(f"Speaking: {text}")
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                self.is_speaking = False
                print("Speech completed.")
                
            except Exception as e:
                print(f"Error during text-to-speech: {e}")
                self.is_speaking = False
        
        if blocking:
            speak_text()
        else:
            # Speak in background thread
            speak_thread = threading.Thread(target=speak_text, daemon=True)
            speak_thread.start()
    
    def speak_to_file(self, text: str, output_path: str) -> bool:
        """
        Convert text to speech and save to file.
        
        Args:
            text (str): Text to convert to speech
            output_path (str): Path to save the audio file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.tts_engine or not text.strip():
            return False
        
        try:
            print(f"Saving speech to file: {output_path}")
            self.tts_engine.save_to_file(text, output_path)
            self.tts_engine.runAndWait()
            print("Speech saved to file.")
            return True
        except Exception as e:
            print(f"Error saving speech to file: {e}")
            return False
    
    def stop_speaking(self):
        """Stop current speech."""
        if self.tts_engine and self.is_speaking:
            try:
                self.tts_engine.stop()
                self.is_speaking = False
            except Exception as e:
                print(f"Error stopping speech: {e}")
    
    def stop_listening(self):
        """Stop continuous listening."""
        self.is_listening = False
    
    def get_available_voices(self) -> list:
        """Get list of available TTS voices."""
        if not self.tts_engine:
            return []
        
        try:
            voices = self.tts_engine.getProperty('voices')
            return [(voice.id, voice.name) for voice in voices] if voices else []
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    def set_voice(self, voice_id: str):
        """Set TTS voice by ID."""
        if not self.tts_engine:
            return
        
        try:
            self.tts_engine.setProperty('voice', voice_id)
        except Exception as e:
            print(f"Error setting voice: {e}")
    
    def set_speech_rate(self, rate: int):
        """Set speech rate (words per minute)."""
        if not self.tts_engine:
            return
        
        try:
            # Clamp rate between reasonable limits
            rate = max(50, min(400, rate))
            self.tts_engine.setProperty('rate', rate)
        except Exception as e:
            print(f"Error setting speech rate: {e}")
    
    def set_volume(self, volume: float):
        """Set speech volume (0.0 to 1.0)."""
        if not self.tts_engine:
            return
        
        try:
            # Clamp volume between 0.0 and 1.0
            volume = max(0.0, min(1.0, volume))
            self.tts_engine.setProperty('volume', volume)
        except Exception as e:
            print(f"Error setting volume: {e}")
    
    def test_microphone(self) -> bool:
        """Test if microphone is working."""
        try:
            with self.microphone as source:
                print("Testing microphone... Say something!")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=2)
                text = self.recognizer.recognize_google(audio)
                print(f"Microphone test successful. Heard: {text}")
                return True
        except Exception as e:
            print(f"Microphone test failed: {e}")
            return False
    
    def test_speakers(self):
        """Test if text-to-speech is working."""
        try:
            self.speak("This is a test of the text-to-speech system.", blocking=True)
            return True
        except Exception as e:
            print(f"Speaker test failed: {e}")
            return False
    
    def get_microphone_list(self) -> list:
        """Get list of available microphones."""
        try:
            mic_list = []
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                mic_list.append((index, name))
            return mic_list
        except Exception as e:
            print(f"Error getting microphone list: {e}")
            return []
    
    def set_microphone(self, device_index: int):
        """Set microphone by device index."""
        try:
            self.microphone = sr.Microphone(device_index=device_index)
            self.setup_microphone()
            return True
        except Exception as e:
            print(f"Error setting microphone: {e}")
            return False

# Utility functions for voice commands
def is_voice_command(text: str, command: str) -> bool:
    """Check if text contains a voice command."""
    return command.lower() in text.lower()

def extract_voice_command(text: str, command: str) -> str:
    """Extract text after a voice command."""
    text_lower = text.lower()
    command_lower = command.lower()
    
    if command_lower in text_lower:
        index = text_lower.find(command_lower)
        return text[index + len(command):].strip()
    return ""

def process_voice_commands(text: str) -> dict:
    """Process common voice commands and return actions."""
    text_lower = text.lower()
    
    commands = {
        'search_history': ['search history', 'find conversation', 'look for'],
        'clear_history': ['clear history', 'delete all', 'remove all'],
        'export_history': ['export history', 'save conversation', 'download history'],
        'capture_image': ['take photo', 'capture image', 'camera'],
        'change_mode': ['dark mode', 'light mode', 'switch theme'],
        'help': ['help', 'what can you do', 'commands'],
        'stop': ['stop', 'quit', 'exit', 'close']
    }
    
    result = {'action': None, 'parameters': None}
    
    for action, triggers in commands.items():
        for trigger in triggers:
            if trigger in text_lower:
                result['action'] = action
                result['parameters'] = extract_voice_command(text, trigger)
                return result
    
    # If no command found, treat as regular chat
    result['action'] = 'chat'
    result['parameters'] = text
    return result

if __name__ == "__main__":
    # Test voice functionality
    voice_manager = VoiceManager()
    
    print("Available microphones:")
    for index, name in voice_manager.get_microphone_list():
        print(f"  {index}: {name}")
    
    print("\\nAvailable voices:")
    for voice_id, name in voice_manager.get_available_voices():
        print(f"  {name}")
    
    # Test microphone (uncomment to test)
    # print("\\nTesting microphone...")
    # voice_manager.test_microphone()
    
    # Test text-to-speech
    print("\\nTesting text-to-speech...")
    voice_manager.test_speakers()
    
    # Test voice input (uncomment to test)
    # print("\\nTesting voice input...")
    # result = voice_manager.listen_once(timeout=5)
    # if result:
    #     print(f"Voice input result: {result}")
    #     voice_manager.speak(f"You said: {result}")