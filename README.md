# AI Chatbot Assistant - Web Application

Advanced AI Chatbot with Image Analysis & Voice powered by Google Gemini AI.

An advanced AI chatbot application that integrates with OpenAI's GPT-4 API to deliver intelligent conversational responses. Features both desktop (CustomTkinter) and web (Streamlit) versions with comprehensive functionality including image analysis, voice interaction, and conversation history management.

## ✨ Features

### 🤖 AI Conversation
- **Intelligent Text Chat**: Powered by Google Gemini AI for natural conversations
- **Context Awareness**: Maintains conversation history for coherent interactions
- **Error Handling**: Robust error management with user-friendly messages

### 🖼️ Image Analysis
- **Visual Recognition**: Upload or capture images for AI analysis using Gemini Vision
- **Multiple Formats**: Supports JPG, JPEG, PNG, GIF, BMP, WEBP
- **Smart Processing**: Automatic image optimization and resizing
- **Camera Integration**: Direct camera capture with auto-analysis

### 🎙️ Voice Features
- **Speech-to-Text**: Voice input using Google Speech Recognition
- **Text-to-Speech**: AI responses can be spoken aloud
- **Auto-Read Mode**: Toggle automatic reading of all AI responses
- **Listen Buttons**: Click to hear any previous AI response on demand
- **Voice Commands**: Natural language voice interactions
- **Microphone/Speaker Testing**: Built-in audio device testing

### 📊 Data Management
- **SQLite Database**: Persistent storage of all conversations
- **Search Functionality**: Find previous conversations by keywords
- **Export Options**: Export chat history to TXT or CSV formats
- **Statistics**: Track conversation metrics and usage patterns

### 🎨 User Interface
- **Modern Design**: Clean, responsive interface
- **Web App**: Streamlit-based web interface
- **Interactive Controls**: Easy-to-use buttons and toggles
- **Real-time Updates**: Instant response display

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- Microphone (optional, for voice features)
- Camera (optional, for image capture)

### Installation

1. **Clone or download the project**
```bash
# If using Git
git clone <repository-url>
cd ai_chatbot_app

# Or extract the downloaded files to a folder
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure your API key**
Create a `.env` file with your Gemini API key:
```bash
# Edit .env file
GEMINI_API_KEY=your-gemini-api-key-here
```

### Running the Application

#### Using the Launcher
```bash
python launcher.py
```
Then select option 1 to launch the web application.

#### Direct Launch
```bash
streamlit run main_web.py
```
Then open http://localhost:8501 in your web browser.

## 📱 Usage Guide

### Web Application

#### Basic Chat
1. Run: `streamlit run main_web.py`
2. Open http://localhost:8501 in your browser
3. Type in the text area and click "Send"
4. View responses in the chat area

#### Image Upload
1. Use the file uploader in the sidebar
2. Select an image file (PNG, JPG, etc.)
3. Ask questions about the uploaded image
4. The AI will analyze the image content

#### Text-to-Speech Features
1. **Auto-Read Mode**: Click "🎤 Auto-Read Responses" in the sidebar to toggle ON/OFF
   - When ON: All AI responses are automatically read aloud
   - When OFF: Use Listen buttons to hear specific responses
2. **Listen Buttons**: Click the "🔊 Listen" button below any AI response to hear it
3. **Voice Input**: Select "Voice" input method and click "🎤 Start Recording" to speak
4. **Test Audio**: Use "🔊 Test Speakers" button to verify audio is working

See [TTS_FEATURES.md](TTS_FEATURES.md) for detailed text-to-speech documentation.

### Common Operations

#### Search Chat History
1. Enter keywords in the search box
2. Click "🔍 Search" 
3. View results in the expanded section

#### Export Conversations
1. Click "💾 Export TXT" or "💾 Export CSV"
2. Files are saved in the application directory
3. TXT format includes timestamps and full conversation
4. CSV format is suitable for data analysis

#### Settings and Troubleshooting
1. Click "⚙️" (desktop) or check Settings section (web)
2. Test microphone and speakers
3. View conversation statistics
4. Check camera availability

## 🛠️ Technical Details

### Architecture
```
ai_chatbot_app/
├── main_desktop.py          # CustomTkinter desktop application
├── main_web.py              # Streamlit web application
├── database.py              # SQLite database management
├── openai_client.py         # OpenAI API integration
├── image_utils.py           # Image processing and camera
├── voice_utils.py           # Speech recognition and TTS
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # Documentation
```

### Database Schema
```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_query TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    query_type TEXT DEFAULT 'text',
    image_path TEXT
);
```

### Dependencies
- **openai**: GPT-4 API integration
- **customtkinter**: Modern desktop GUI framework
- **streamlit**: Web application framework
- **opencv-python**: Camera and image processing
- **Pillow**: Image manipulation
- **speech_recognition**: Voice input processing
- **pyttsx3**: Text-to-speech output
- **pandas**: Data export functionality
- **python-dotenv**: Environment variable management

### Configuration
The application uses environment variables for configuration:
- `OPENAI_API_KEY`: Your OpenAI API key (required)

## 🔧 Advanced Features

### Voice Commands
The application supports natural language voice commands:
- "Search history for [topic]"
- "Clear history"
- "Export history"
- "Take photo" / "Capture image"
- "Dark mode" / "Light mode"
- "Help"

### Image Processing
- Automatic format conversion to RGB
- Smart resizing for optimal AI processing
- Support for various image formats
- Thumbnail generation for display

### Database Features
- Automatic database initialization
- Conversation search with SQL LIKE queries
- Export to multiple formats (TXT, CSV)
- Statistical analysis of usage patterns
- Cleanup and maintenance functions

### Error Handling
- Comprehensive exception handling
- User-friendly error messages
- Graceful degradation when features unavailable
- Retry logic for API calls

## 🐛 Troubleshooting

### Common Issues

#### API Key Problems
```
Error: OpenAI API key not found in environment variables
```
**Solution**: Check that the `.env` file contains your valid API key.

#### Voice Issues
```
Error: Could not understand the audio
```
**Solutions**:
- Check microphone permissions
- Ensure microphone is working
- Test microphone in settings
- Speak clearly and close to microphone

#### Camera Problems
```
Error: Could not open camera
```
**Solutions**:
- Check camera permissions
- Ensure camera is not being used by another application
- Try disconnecting/reconnecting camera
- Restart the application

#### Image Processing Errors
```
Error: Failed to load image
```
**Solutions**:
- Use supported image formats (JPG, PNG, etc.)
- Ensure image file is not corrupted
- Check file permissions
- Try a different image

#### Installation Issues
```
ModuleNotFoundError: No module named 'customtkinter'
```
**Solution**: Install requirements: `pip install -r requirements.txt`

### Performance Tips
1. **Large Images**: Images are automatically resized, but smaller images process faster
2. **Long Conversations**: Clear chat history periodically to maintain performance
3. **Voice Response**: Disable voice output if not needed to reduce processing time
4. **Database Size**: Export and clear history periodically if using extensively

### Limitations
- **Web Voice Features**: Limited by browser security policies
- **Camera in Web**: Not available in Streamlit version
- **Concurrent Users**: Desktop app is single-user; web app supports multiple sessions
- **Image Size**: Very large images (>10MB) may cause processing delays

## 📊 Usage Statistics

The application tracks:
- Total conversations
- Conversations by type (text/image)
- Recent activity (last 7 days)
- Token usage (displayed per response)

Access statistics through:
- Desktop: Settings window (⚙️ button)
- Web: Statistics section in sidebar

## 🔐 Security Notes

- **API Key**: Stored securely in `.env` file, not in code
- **Local Storage**: All data stored locally in SQLite database
- **No Cloud Storage**: Images and conversations remain on your device
- **Privacy**: No data sent to third parties except OpenAI API

## 🤝 Support

### Getting Help
1. **Built-in Help**: Press F1 (desktop) or check Help section (web)
2. **Error Messages**: Check console output for detailed error information
3. **Logs**: Application prints status and error information to console

### Feature Requests
This is a complete implementation with all requested features:
- ✅ Text conversations with GPT-4
- ✅ Image analysis with GPT-4 Vision
- ✅ Voice input and output
- ✅ Modern responsive UI (both desktop and web)
- ✅ SQLite database with search
- ✅ Export functionality (TXT/CSV)
- ✅ Dark/light theme toggle
- ✅ Camera integration
- ✅ Secure API key management

## 🚀 Deployment on Render

### Prerequisites
- A GitHub account with this repository
- A Render account (free tier available)
- A Google Gemini API key

### Deployment Steps

1. **Push your code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create a new Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository: `vedantkerkar68-blip/chat_bot`

3. **Configure the Service**
   - **Name**: `ai-chatbot-app` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run main_web.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
   - **Plan**: Free (or choose a paid plan)

4. **Set Environment Variables**
   - Go to "Environment" section
   - Add a new environment variable:
     - **Key**: `GEMINI_API_KEY`
     - **Value**: Your Google Gemini API key
   - Click "Save Changes"

5. **Deploy**
   - Click "Create Web Service"
   - Wait for the build to complete (usually 2-3 minutes)
   - Your app will be live at: `https://your-app-name.onrender.com`

### Using render.yaml (Alternative Method)

If you prefer using the `render.yaml` file:
1. The repository already includes `render.yaml`
2. Go to Render Dashboard → "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect and use `render.yaml`
5. Set the `GEMINI_API_KEY` environment variable in the dashboard

### Important Notes for Render Deployment

- **Database**: SQLite databases are ephemeral on Render's free tier. Data may be lost on restarts. For production, consider using PostgreSQL or another persistent database.
- **Voice Features**: Some voice features may have limitations in a web environment
- **Camera Features**: Camera capture is not available in the web version
- **File Uploads**: Image uploads work, but files are stored temporarily
- **Free Tier Limitations**: 
  - Services spin down after 15 minutes of inactivity
  - First request after spin-down may take 30-60 seconds
  - Upgrade to a paid plan for always-on service

### Troubleshooting Deployment

**Build fails:**
- Check that all dependencies in `requirements.txt` are valid
- Ensure Python version compatibility

**App crashes on start:**
- Verify `GEMINI_API_KEY` is set correctly
- Check Render logs for error messages
- Ensure start command is correct

**App doesn't respond:**
- Wait 30-60 seconds for first request (free tier spin-up)
- Check Render dashboard for service status
- Verify the service is not sleeping

## 📄 License

This project is created for educational and personal use. Please ensure compliance with OpenAI's usage policies when using their API services.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 and Vision API
- **CustomTkinter** for modern desktop GUI framework
- **Streamlit** for easy web app development
- **Contributors** to all open-source libraries used

---

**Enjoy your AI Chatbot Assistant! 🤖✨**