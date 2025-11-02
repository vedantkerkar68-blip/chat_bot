#!/usr/bin/env python3
"""
AI Chatbot Assistant Launcher
Simple launcher script to start either the desktop or web version of the application.
"""

import sys
import subprocess
import os
from pathlib import Path

def print_banner():
    """Print application banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                  🤖 AI Chatbot Assistant 🤖                  ║
    ║                                                              ║
    ║        Advanced AI Chatbot with Image Analysis & Voice      ║
    ║                    Powered by Google Gemini AI              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check if required files exist."""
    required_files = [
        'main_web.py',
        'database.py',
        'gemini_client.py',
        'image_utils.py',
        'voice_utils.py',
        'requirements.txt',
        '.env'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all files are present in the application directory.")
        return False
    
    return True

def check_api_key():
    """Check if Gemini API key is configured."""
    try:
        with open('.env', 'r') as f:
            content = f.read()
            if 'GEMINI_API_KEY=' in content and 'AIza' in content:
                return True
            else:
                print("❌ Gemini API key not found in .env file")
                print("Please ensure your API key is properly configured in .env file")
                return False
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        print(f"Error output: {e.stderr}")
        return False


def launch_web():
    """Launch the web application."""
    print("🌐 Launching Web Application...")
    print("Opening Streamlit app... Your browser should open automatically.")
    print("If not, navigate to: http://localhost:8501")
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'main_web.py'])
    except KeyboardInterrupt:
        print("\n👋 Web application closed by user")
    except Exception as e:
        print(f"❌ Error launching web app: {e}")

def test_basic_functionality():
    """Test basic application functionality."""
    print("🧪 Testing basic functionality...")
    
    try:
        # Test database
        from database import DatabaseManager
        db = DatabaseManager()
        print("✅ Database connection: OK")
        
        # Test Gemini client initialization
        from gemini_client import GeminiClient
        client = GeminiClient()
        print("✅ Gemini client initialization: OK")
        
        # Test image processor
        from image_utils import ImageProcessor
        processor = ImageProcessor()
        print("✅ Image processor: OK")
        
        # Test voice manager initialization
        from voice_utils import VoiceManager
        voice = VoiceManager()
        print("✅ Voice manager: OK")
        
        print("✅ All core components initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False

def main():
    """Main launcher function."""
    print_banner()
    
    # Check if we're in the right directory
    if not os.path.exists('main_web.py'):
        print("❌ Error: Please run this script from the ai_chatbot_app directory")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check API key
    if not check_api_key():
        sys.exit(1)
    
    while True:
        print("\n" + "="*60)
        print("🚀 AI Chatbot Assistant - Web Application")
        print("="*60)
        print("1. 🌐 Launch Web Application (Streamlit)")
        print("2. 📦 Install/Update Requirements")
        print("3. 🧪 Test Basic Functionality")
        print("4. ❌ Exit")
        print("="*60)
        
        try:
            choice = input("\n👉 Enter your choice (1-4): ").strip()
            
            if choice == '1':
                launch_web()
            elif choice == '2':
                if install_requirements():
                    print("\n✅ Requirements updated successfully!")
                else:
                    print("\n❌ Failed to update requirements")
            elif choice == '3':
                test_basic_functionality()
            elif choice == '4':
                print("\n👋 Goodbye! Thanks for using AI Chatbot Assistant!")
                break
            else:
                print("\n❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using AI Chatbot Assistant!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()