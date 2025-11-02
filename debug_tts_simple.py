"""
Simple TTS Debug Script
Run this to verify your text-to-speech is working at all
"""
import sys

print("Testing Text-to-Speech...")
print("-" * 50)

try:
    # Test 1: Import voice_utils
    print("\n✓ Test 1: Importing voice_utils...")
    from voice_utils import VoiceManager
    print("  SUCCESS: voice_utils imported")
    
    # Test 2: Initialize VoiceManager
    print("\n✓ Test 2: Initializing VoiceManager...")
    voice = VoiceManager()
    print("  SUCCESS: VoiceManager initialized")
    
    # Test 3: Simple TTS test
    print("\n✓ Test 3: Testing text-to-speech (you should hear this)...")
    test_text = "Hello, this is a test. Can you hear me?"
    print(f"  Speaking: '{test_text}'")
    voice.speak(test_text, blocking=True)
    print("  SUCCESS: Audio played")
    
    # Test 4: Non-blocking TTS
    print("\n✓ Test 4: Testing non-blocking TTS...")
    import threading
    test_text2 = "This is non-blocking speech"
    print(f"  Speaking: '{test_text2}'")
    thread = threading.Thread(target=voice.speak, args=(test_text2, False), daemon=True)
    thread.start()
    thread.join(timeout=5)
    print("  SUCCESS: Non-blocking audio initiated")
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("=" * 50)
    print("\nYour TTS is working correctly.")
    print("If you heard the audio, the problem is in the Streamlit integration.")
    
except ImportError as e:
    print(f"\n❌ IMPORT ERROR: {e}")
    print("\nFix: Install required packages:")
    print("  pip install pyttsx3 speech_recognition")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nPossible issues:")
    print("1. No audio output device")
    print("2. Audio drivers not installed")
    print("3. pyttsx3 not properly configured")
    print("\nTry:")
    print("  - Check system volume")
    print("  - Check audio device is working")
    print("  - Reinstall: pip uninstall pyttsx3 && pip install pyttsx3")
    sys.exit(1)
