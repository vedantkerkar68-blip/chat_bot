import streamlit as st
import os
import tempfile
from datetime import datetime
import pandas as pd
from PIL import Image
import cv2
import base64
import threading
import time

# Import our custom modules
from database import DatabaseManager
from gemini_client import GeminiClient
from image_utils import ImageProcessor, CameraManager
from voice_utils import VoiceManager

# Configure Streamlit page
st.set_page_config(
    page_title="AI Chatbot Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "db" not in st.session_state:
    st.session_state.db = DatabaseManager()

if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = GeminiClient()

if "image_processor" not in st.session_state:
    st.session_state.image_processor = ImageProcessor()

if "camera_manager" not in st.session_state:
    st.session_state.camera_manager = CameraManager()

if "voice_manager" not in st.session_state:
    st.session_state.voice_manager = VoiceManager()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_image" not in st.session_state:
    st.session_state.current_image = None

if "current_image_path" not in st.session_state:
    st.session_state.current_image_path = None

if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = False

if "auto_read_enabled" not in st.session_state:
    st.session_state.auto_read_enabled = False

if "message_counter" not in st.session_state:
    st.session_state.message_counter = 0

if "play_message_id" not in st.session_state:
    st.session_state.play_message_id = None

if "audio_to_play" not in st.session_state:
    st.session_state.audio_to_play = None

if "is_playing_audio" not in st.session_state:
    st.session_state.is_playing_audio = False

if "tts_process" not in st.session_state:
    st.session_state.tts_process = None

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        display: flex;
        flex-direction: column;
    }
    /*background-color: #e3f2fd;*/
    .user-message {
        
        align-self: flex-end;
        max-width: 80%;
        margin-left: auto;
    }
    /*background-color: #f5f5f5;*/
    .assistant-message {
        
        align-self: flex-start;
        max-width: 80%;
    }
    
    .message-header {
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .user-header {
        color: #1976d2;
    }
    
    .assistant-header {
        color: #388e3c;
    }
    
    .stButton > button {
        width: 100%;
    }
    
    .image-container {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def stop_tts():
    """Stop any currently playing TTS."""
    if st.session_state.tts_process:
        try:
            st.session_state.tts_process.kill()
            st.session_state.tts_process = None
        except:
            pass

def speak_text_nonblocking(text):
    """Speak the given text using text-to-speech in a background process."""
    try:
        # Stop any currently playing audio first
        stop_tts()
        
        voice_manager = st.session_state.voice_manager
        # Start speech in a separate thread that won't be interrupted
        import subprocess
        import sys
        
        # Create a simple Python script to run TTS
        script = f'''
import pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate", 200)
engine.setProperty("volume", 0.9)
engine.say("""{text}""")
engine.runAndWait()
'''
        # Run in subprocess to avoid Streamlit interference
        process = subprocess.Popen([sys.executable, "-c", script], 
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        st.session_state.tts_process = process
    except Exception as e:
        st.error(f"Error with text-to-speech: {e}")

def request_play_message(message_id):
    """Request to play a specific message."""
    # If clicking the same message that's playing, stop it
    if st.session_state.play_message_id == message_id:
        stop_tts()
        st.session_state.play_message_id = None
    else:
        # Otherwise play the new message
        st.session_state.play_message_id = message_id

def display_message(role, content, timestamp=None, message_index=None):
    """Display a chat message with proper styling."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M:%S")
    
    message_class = "user-message" if role == "user" else "assistant-message"
    header_class = "user-header" if role == "user" else "assistant-header"
    role_display = "You" if role == "user" else "AI Assistant"
    
    # Create a container for the message
    with st.container():
        st.markdown(f"""
        <div class="chat-message {message_class}">
            <div class="message-header {header_class}">
                {role_display} • {timestamp}
            </div>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add Listen and Stop buttons for AI messages
        if role == "assistant":
            col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.55, 0.15])
            with col1:
                # Use unique message_index for button key
                st.button(
                    "🔊 Listen", 
                    key=f"listen_btn_{message_index}", 
                    help="Click to hear this response",
                    on_click=request_play_message,
                    args=(message_index,)
                )
            with col2:
                if st.button(
                    "⏹️ Stop",
                    key=f"stop_btn_{message_index}",
                    help="Stop audio playback",
                    type="secondary"
                ):
                    stop_tts()

def display_chat_history():
    """Display all messages in the chat history."""
    for message in st.session_state.messages:
        display_message(
            message["role"], 
            message["content"], 
            message.get("timestamp", ""),
            message_index=message.get("id", 0)
        )

def check_and_play_audio():
    """Check if we need to play audio and do it."""
    if st.session_state.play_message_id is not None:
        # Find the message to play
        for message in st.session_state.messages:
            if message.get("id") == st.session_state.play_message_id and message["role"] == "assistant":
                st.info("🔊 Playing audio...")
                speak_text_nonblocking(message["content"])
                break
        # Reset the play request
        st.session_state.play_message_id = None

def add_message(role, content):
    """Add a message to the chat history."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.message_counter += 1
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": timestamp,
        "id": st.session_state.message_counter
    })

def process_user_input(user_input):
    """Process user input and get AI response."""
    try:
        # Add user message
        add_message("user", user_input)
        
        # Show processing message
        with st.spinner("AI is thinking..."):
            query_type = "image" if st.session_state.current_image_path else "text"
            
            if st.session_state.current_image_path:
                # Image analysis
                response = st.session_state.gemini_client.analyze_image(
                    st.session_state.current_image_path, user_input
                )
            else:
                # Text conversation
                response = st.session_state.gemini_client.get_text_response(user_input)
            
            if response["success"]:
                ai_response = response["response"]
                add_message("assistant", ai_response)
                
                # Save to database
                st.session_state.db.add_conversation(
                    user_query=user_input,
                    ai_response=ai_response,
                    query_type=query_type,
                    image_path=st.session_state.current_image_path
                )
                
                # Voice response if auto-read is enabled
                if st.session_state.auto_read_enabled:
                    try:
                        speak_text_nonblocking(ai_response)
                    except Exception as e:
                        st.warning(f"Voice output error: {e}")
                
                st.success(f"Response received! Used {response['usage']['total_tokens']} tokens.")
            else:
                error_msg = f"Error: {response['error']}"
                add_message("assistant", error_msg)
                st.error("Failed to get AI response")
                
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        add_message("assistant", error_msg)
        st.error(f"Error processing message: {e}")

def main():
    """Main Streamlit application."""
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Chatbot Assistant</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Controls")
        
        # Auto-read toggle
        st.subheader("🔊 Text-to-Speech")
        if st.button("🎤 Auto-Read Responses" + (" ON" if st.session_state.auto_read_enabled else " OFF")):
            st.session_state.auto_read_enabled = not st.session_state.auto_read_enabled
            if st.session_state.auto_read_enabled:
                st.success("Auto-read enabled! AI responses will be read aloud automatically.")
            else:
                st.info("Auto-read disabled. Use 🔊 Listen buttons to hear responses.")
        
        st.caption("💡 Tip: Use 🔊 Listen buttons below each AI response to hear them anytime!")
        
        # Image upload section
        st.header("📷 Image Analysis")
        uploaded_file = st.file_uploader(
            "Upload an image for analysis",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
            key="image_uploader"
        )
        
        if uploaded_file:
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    temp_path = tmp_file.name
                
                # Process image
                processed_path = st.session_state.image_processor.prepare_for_ai_analysis(temp_path)
                st.session_state.current_image_path = processed_path
                st.session_state.current_image = Image.open(temp_path)
                
                # Display image
                st.image(st.session_state.current_image, caption="Uploaded Image", use_container_width=True)
                
                # Get image info
                info = st.session_state.image_processor.get_image_info(temp_path)
                st.info(f"Image: {info.get('width', 0)}×{info.get('height', 0)} pixels")
                
            except Exception as e:
                st.error(f"Error processing image: {e}")
        
        # Camera capture
        if st.button("📸 Capture from Camera"):
            try:
                with st.spinner("Opening camera... Please allow camera access if prompted."):
                    # Use headless camera capture for web
                    captured_path = st.session_state.image_processor.capture_from_camera_headless()
                    if captured_path:
                        # Process the captured image
                        processed_path = st.session_state.image_processor.prepare_for_ai_analysis(captured_path)
                        st.session_state.current_image_path = processed_path
                        st.session_state.current_image = Image.open(captured_path)
                        
                        # Display the captured image
                        st.image(st.session_state.current_image, caption="Captured Image", use_container_width=True)
                        
                        # Automatically analyze the image
                        with st.spinner("Analyzing captured image..."):
                            analysis_response = st.session_state.gemini_client.analyze_image(
                                processed_path, "What do you see in this image? Please describe it in detail."
                            )
                            
                            if analysis_response["success"]:
                                st.success("Image captured and analyzed!")
                                
                                # Add to chat messages for display
                                add_message("user", "📸 Camera capture - What do you see?")
                                add_message("assistant", analysis_response['response'])
                                
                                # Save the analysis to database
                                st.session_state.db.add_conversation(
                                    user_query="Camera capture - What do you see?",
                                    ai_response=analysis_response['response'],
                                    query_type="image",
                                    image_path=processed_path
                                )
                                
                                # Voice response if auto-read is enabled
                                if st.session_state.auto_read_enabled:
                                    try:
                                        speak_text_nonblocking(analysis_response['response'])
                                    except Exception as e:
                                        st.warning(f"Voice output error: {e}")
                            else:
                                st.error(f"Failed to analyze image: {analysis_response['error']}")
                        
                        st.rerun()
                    else:
                        st.error("Failed to capture image from camera")
            except Exception as e:
                st.error(f"Camera capture error: {e}")
                st.info("If camera doesn't work, try uploading an image instead.")
        
        # Clear image
        if st.session_state.current_image and st.button("❌ Clear Image"):
            st.session_state.current_image = None
            st.session_state.current_image_path = None
            st.success("Image cleared!")
            st.rerun()
        
        # History section
        st.header("📋 Chat History")
        
        # Search
        search_term = st.text_input("🔍 Search conversations", key="search_input")
        if st.button("Search") and search_term:
            results = st.session_state.db.search_conversations(search_term)
            if results:
                st.success(f"Found {len(results)} results")
                with st.expander("Search Results"):
                    for i, result in enumerate(results[:10]):  # Show first 10 results
                        id_, user_query, ai_response, timestamp, query_type, image_path = result
                        st.write(f"**{i+1}. {timestamp}** ({query_type})")
                        st.write(f"**You:** {user_query}")
                        st.write(f"**AI:** {ai_response}")
                        st.write("---")
            else:
                st.info("No conversations found")
        
        
        # Clear history
        if st.button("🗑️ Clear All History"):
            if st.session_state.db.clear_all_history():
                st.success("History cleared!")
            else:
                st.error("Failed to clear history")
        
        # Statistics
        st.header("📊 Statistics")
        try:
            stats = st.session_state.db.get_conversation_stats()
            st.metric("Total Conversations", stats.get('total_conversations', 0))
            st.metric("Recent (7 days)", stats.get('recent_conversations', 0))
            
            # Show conversation types
            by_type = stats.get('by_type', {})
            if by_type:
                st.write("**By Type:**")
                for conv_type, count in by_type.items():
                    st.write(f"• {conv_type}: {count}")
        except Exception as e:
            st.error(f"Error loading statistics: {e}")
        
        # Settings
        st.header("⚙️ Settings")
        if st.button("🎤 Test Microphone"):
            try:
                result = st.session_state.voice_manager.test_microphone()
                if result:
                    st.success("Microphone test successful!")
                else:
                    st.error("Microphone test failed")
            except Exception as e:
                st.error(f"Microphone test error: {e}")
        
        if st.button("🔊 Test Speakers"):
            try:
                st.session_state.voice_manager.test_speakers()
                st.success("Speaker test completed!")
            except Exception as e:
                st.error(f"Speaker test error: {e}")
        
        # Camera status
        camera_status = "Available" if st.session_state.camera_manager.camera_available else "Not Available"
        st.info(f"Camera Status: {camera_status}")
    
    # Main chat area
    st.header("💬 Chat")
    
    # Display current image if loaded
    if st.session_state.current_image:
        st.image(st.session_state.current_image, caption="Current Image for Analysis", width=300)
    
    # Chat history container
    chat_container = st.container()
    
    with chat_container:
        display_chat_history()
    
    # Check if audio should be played
    check_and_play_audio()
    
    # Chat input
    st.markdown("---")
    
    # Input methods
    input_method = st.radio("Input Method:", ["Text", "Voice"], horizontal=True)
    
    if input_method == "Text":
        # Text input
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            user_input = st.text_area(
                "Type your message:",
                height=100,
                placeholder="Ask me anything or describe what you want to know about the image...",
                key="text_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
            if st.button("Send", type="primary"):
                if user_input.strip():
                    process_user_input(user_input)
                    st.rerun()
                else:
                    st.warning("Please enter a message")
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
            if st.button("🔄 Clear Chat", key="clear_chat_text"):
                st.session_state.messages = []
                st.session_state.current_image = None
                st.session_state.current_image_path = None
                st.success("Chat cleared!")
                st.rerun()
    
    else:
        # Voice input
        st.info("Voice input in web version requires microphone permissions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎤 Start Recording"):
                try:
                    with st.spinner("Listening... Please speak now"):
                        result = st.session_state.voice_manager.listen_once(timeout=10)
                        if result:
                            st.success(f"Recognized: {result}")
                            process_user_input(result)
                            st.rerun()
                        else:
                            st.warning("No speech detected")
                except Exception as e:
                    st.error(f"Voice input error: {e}")
        
        with col2:
            if st.button("🔄 Clear Chat"):
                st.session_state.messages = []
                st.session_state.current_image = None
                st.session_state.current_image_path = None
                st.success("Chat cleared!")
                st.rerun()
    
    # Help section
    with st.expander("ℹ️ Help & Instructions"):
        st.markdown("""
        ### How to use this AI Chatbot:
        
        **💬 Text Chat:**
        - Type your message in the text area and click "Send"
        - The AI will respond based on your input
        
        **📷 Image Analysis:**
        - Upload an image using the file uploader in the sidebar
        - Or capture directly from your camera (automatically analyzes what it sees)
        - Ask questions about uploaded/captured images
        - The AI can identify objects, read text, describe scenes, and more
        
        **🔊 Text-to-Speech Features:**
        - Enable "Auto-Read Responses" to automatically hear all AI responses
        - Click the 🔊 Listen button below any AI message to hear it
        - Use voice input to speak your questions (requires microphone)
        - Test your microphone and speakers in the settings
        
        **📋 History Management:**
        - Search through your conversation history
        - Clear history when needed
        
        **⚙️ Tips:**
        - Be specific in your questions for better responses
        - Use clear, high-quality images for better analysis
        - Enable voice for a hands-free experience
        - Search through history to find previous conversations
        
        **🔧 Troubleshooting:**
        - If voice features don't work, check browser microphone permissions
        - Large images are automatically resized for processing
        - Clear browser cache if you experience issues
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>AI Chatbot Assistant - Powered by Google Gemini AI</p>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.info("Please refresh the page and try again.")