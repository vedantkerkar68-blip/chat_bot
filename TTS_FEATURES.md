# Text-to-Speech Features

## Overview
Your AI Chatbot now supports reading responses aloud with two convenient options:

### 1. **Auto-Read Mode** 🎤
- **Location**: Sidebar → Text-to-Speech section
- **How to use**: Click "🎤 Auto-Read Responses" button to toggle ON/OFF
- **What it does**: Automatically reads every AI response aloud as soon as it's generated
- **Best for**: Hands-free operation, accessibility, multitasking

### 2. **Manual Listen Button** 🔊
- **Location**: Below each AI response message
- **How to use**: Click the "🔊 Listen" button next to any AI message
- **What it does**: Reads that specific response aloud on demand
- **Best for**: Selective listening, reviewing previous responses

## Features

✅ **Natural Voice**: Uses your system's built-in text-to-speech engine
✅ **Background Processing**: Continues reading while you can still interact with the app
✅ **Previous Messages**: Listen to any previous AI response using its Listen button
✅ **Control**: Easy toggle between auto-read and manual modes

## How to Use

### Enable Auto-Read
1. Open the web application
2. Look for the sidebar on the left
3. Find the "🔊 Text-to-Speech" section
4. Click "🎤 Auto-Read Responses OFF" to turn it ON
5. Now all AI responses will be read automatically!

### Listen to Individual Messages
1. Scroll through your chat history
2. Find the AI response you want to hear
3. Click the "🔊 Listen" button below that message
4. The text will be read aloud

## Settings

You can customize the voice settings:
- **Test Speakers**: Use the "🔊 Test Speakers" button in Settings
- **Voice Speed & Volume**: These are controlled by your system settings
  - **Windows**: Settings → Time & Language → Speech
  - **Mac**: System Preferences → Accessibility → Spoken Content

## Troubleshooting

**Problem**: No sound when clicking Listen
- **Solution**: Check your system volume and speaker connections
- Click "🔊 Test Speakers" in the Settings section

**Problem**: Voice sounds robotic or unclear
- **Solution**: Adjust voice settings in your operating system settings

**Problem**: Auto-read doesn't work
- **Solution**: 
  1. Make sure Auto-Read is toggled ON
  2. Test speakers using the test button
  3. Check that pyttsx3 is installed: `pip install pyttsx3`

## Technical Details

- **Engine**: Uses `pyttsx3` library with your system's TTS engine
- **Windows**: Uses SAPI5 (Microsoft Speech API)
- **Threading**: Runs in background to avoid blocking the UI
- **Compatibility**: Works offline, no internet required for TTS

## Tips

💡 Use Auto-Read mode while:
- Cooking or doing household tasks
- Exercising
- Working on something else
- Accessibility needs

💡 Use Listen buttons for:
- Reviewing specific responses
- Checking pronunciation
- Sharing responses with others
- When you want selective audio
