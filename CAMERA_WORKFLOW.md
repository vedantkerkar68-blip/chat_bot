# 📸 Camera Capture Workflow

## Web Application (Streamlit)

### User Action:
1. Click "📸 Capture from Camera" button in sidebar

### System Response:
1. **Camera Activation**: Browser requests camera permission
2. **Image Capture**: System captures image using headless camera capture
3. **Image Processing**: Image is processed and prepared for AI analysis
4. **Image Display**: Captured image is shown to user
5. **AI Analysis**: Gemini AI analyzes the image with prompt "What do you see in this image? Please describe it in detail."
6. **Chat Integration**: 
   - Adds user message: "📸 Camera capture - What do you see?"
   - Adds AI response with detailed description
7. **Database Storage**: Saves conversation to SQLite database
8. **Voice Output** (if enabled): AI speaks the description
9. **UI Update**: Page refreshes to show new chat messages

## Desktop Application (CustomTkinter)

### User Action:
1. Click "📷 Capture" button in top toolbar

### System Response:
1. **Camera Window**: OpenCV camera window opens
2. **User Interaction**: User presses SPACE to capture or ESC to cancel
3. **Image Capture**: System captures and saves image
4. **Image Display**: Shows image in sidebar preview
5. **AI Analysis**: Gemini AI analyzes the image
6. **Chat Integration**:
   - Adds user message: "📸 Camera capture - What do you see?"
   - Adds AI response with detailed description
7. **Database Storage**: Saves conversation to SQLite database
8. **Voice Output** (if enabled): AI speaks the description
9. **Status Update**: Shows success message with token count

## Data Storage

Both versions save to SQLite database with:
- **user_query**: "Camera capture - What do you see?"
- **ai_response**: AI's detailed description
- **query_type**: "image"
- **image_path**: Path to captured image
- **timestamp**: Current date/time

## User Experience

### What User Sees:
- Image preview of what was captured
- Chat message showing the capture action
- AI's detailed analysis in chat
- Analysis saved in searchable history

### What User Hears (if voice enabled):
- AI speaks the analysis description aloud

This creates a seamless experience where camera capture automatically generates an AI analysis that becomes part of the conversation flow.