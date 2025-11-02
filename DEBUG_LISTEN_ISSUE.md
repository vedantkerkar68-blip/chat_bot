# Debug: Listen Button Not Working

## Quick Test

### Step 1: Test TTS Engine Directly
```bash
python debug_tts_simple.py
```

**Expected**: You should hear "Hello, this is a test. Can you hear me?"

- ✅ **If you hear it**: TTS engine works, problem is in Streamlit integration
- ❌ **If you don't hear it**: TTS engine issue, see fixes below

### Step 2: Test in Streamlit App
```bash
streamlit run main_web.py
```

1. Go to sidebar → Settings
2. Click "🔊 Test Speakers"
3. **Expected**: You should hear "This is a test of the text-to-speech system"

- ✅ **If you hear it**: VoiceManager works in Streamlit
- ❌ **If you don't**: Session state issue

### Step 3: Test Listen Buttons
1. Send message: "hi"
2. Wait for response
3. Click 🔊 Listen button
4. Check browser console (F12) for errors

## Common Issues & Fixes

### Issue 1: No Audio Device
**Symptom**: No sound at all, even in debug script

**Fix**:
```bash
# Windows: Check sound settings
# Settings → System → Sound → Output device

# Verify audio is working in other apps (YouTube, etc.)
```

### Issue 2: pyttsx3 Not Working
**Symptom**: Errors mentioning pyttsx3

**Fix**:
```bash
pip uninstall pyttsx3
pip install pyttsx3==2.90
```

### Issue 3: Threading Issue
**Symptom**: First button works, others don't

**Current Fix Applied**:
- Using `on_click` callbacks
- Session state for play requests
- Non-blocking audio execution

**To Verify**:
1. Open browser console (F12)
2. Click Listen button
3. Look for JavaScript errors

### Issue 4: Streamlit Rerun Issue
**Symptom**: Button clicks don't trigger anything

**Debug**:
Add this temporarily to `main_web.py` after line 450:

```python
# Check if audio should be played
if st.session_state.play_message_id is not None:
    st.write(f"DEBUG: Should play message {st.session_state.play_message_id}")
check_and_play_audio()
```

**Expected**: You should see "DEBUG: Should play message X" when clicking Listen

## Current Implementation

### How It Should Work:

1. **Click Button** → Triggers `request_play_message(message_id)`
2. **Set State** → `st.session_state.play_message_id = message_id`
3. **Page Reruns** → State persists
4. **Check State** → `check_and_play_audio()` runs
5. **Play Audio** → Finds message and calls `speak_text()`
6. **Reset State** → Sets `play_message_id = None`

### Verify Each Step:

```python
# Add to check_and_play_audio() function:
def check_and_play_audio():
    st.write(f"DEBUG: play_message_id = {st.session_state.play_message_id}")  # DEBUG
    if st.session_state.play_message_id is not None:
        st.write(f"DEBUG: Looking for message {st.session_state.play_message_id}")  # DEBUG
        for message in st.session_state.messages:
            if message.get("id") == st.session_state.play_message_id:
                st.write(f"DEBUG: Found message: {message['content'][:50]}...")  # DEBUG
                st.toast("🔊 Playing audio...", icon="🔊")
                speak_text(message["content"])
                break
        st.session_state.play_message_id = None
```

## What Changed in Latest Fix:

1. ✅ Changed `speak_text()` to use `blocking=False`
2. ✅ Separated `check_and_play_audio()` from `display_chat_history()`
3. ✅ Call `check_and_play_audio()` after displaying messages
4. ✅ Using `st.toast()` for feedback instead of `st.info()`

## If Still Not Working:

### Try This Workaround:

Replace the button with a selectbox:

```python
# In display_message function:
if role == "assistant":
    if st.button("🔊 Listen", key=f"listen_{message_index}"):
        # Play immediately instead of using callback
        import threading
        voice_manager = st.session_state.voice_manager
        threading.Thread(
            target=voice_manager.speak, 
            args=(content, False), 
            daemon=True
        ).start()
        st.toast("🔊 Playing...", icon="🔊")
```

## Contact Info

If none of this works, provide:
1. Output of `python debug_tts_simple.py`
2. Any error messages from browser console (F12)
3. Any error messages from terminal running Streamlit
4. Windows version and Python version

---

**Last Updated**: With callback-based implementation
