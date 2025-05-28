import requests
from elevenlabs.client import ElevenLabs
from streamlit_mic_recorder import mic_recorder
import streamlit as st
import io
from io import BytesIO
import time

# API Keys for Voice AI Assistant
API_KEY_MUNSIT = "sk-ctxt-55aab0ddf2334452b0a44872c7c54b39"
API_KEY_VOICEFLOW = "VF.DM.681d292aea78babcc654acaf.JSuEQdV5KSHXu3px"
ELEVENLABS_API_KEY = "sk_83d455e3ed2bc6a6169df3fb04a6926e6852c02530007797"
VOICE_ID = "IES4nrmZdUBHByLBde0P"
VOICEFLOW_USER_ID = "default-user"

# Record audio using Streamlit mic recorder
def record_audio():
    st.markdown("### Recording Instructions:")
    st.markdown("""

    1. Click the microphone button below

    2. When recording, speak clearly into your microphone

    3. Click the button again to stop recording

    4. Wait for the audio to process

    """)
    
    if 'recorder_key' not in st.session_state:
        st.session_state.recorder_key = 'recorder_' + str(int(time.time()))
    if 'audio_bytes' not in st.session_state:
        st.session_state.audio_bytes = None
    

    def audio_callback():
        if st.session_state[st.session_state.recorder_key + '_output']:
            st.session_state.audio_bytes = st.session_state[st.session_state.recorder_key + '_output']['bytes']

    recorder_container = st.container()

    with recorder_container:
        mic_recorder(
            start_prompt="Start Recording",
            stop_prompt="Stop Recording", 
            key=st.session_state.recorder_key,
            callback=audio_callback,
            format="wav",
        )
    if st.session_state.audio_bytes is not None:
        st.audio(st.session_state.audio_bytes, format="audio/wav")
        return st.session_state.audio_bytes
    st.info("Click the button to start recording...")
    return None

# Transcribe using Munsit API
def transcribe_with_munsit(audio_bytes):
    print(audio_bytes[:500])
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY_MUNSIT}"
        }

        files = {
            "file": ("audio.wav", io.BytesIO(audio_bytes), "audio/wav")
        }
        data = {
            "model": "munsit-1"
        }
        response = requests.post(
            "https://api.cntxt.tools/audio/transcribe",
            headers=headers,
            files=files,
            data=data,
        )
        response.raise_for_status()
        result = response.json()
        text = result["data"]["transcription"]
        return text
    except Exception as e:
        st.error(f"Transcription API error: {str(e)}")
        return None

# Interact with Voiceflow
def interact_with_voiceflow(user_input):
    headers = {
        "Authorization": API_KEY_VOICEFLOW,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "request": {
            "type": "text",
            "payload": user_input
        }
    }

    response = requests.post(
        f"https://general-runtime.voiceflow.com/state/user/{VOICEFLOW_USER_ID}/interact",
        json=payload,
        headers=headers,
        stream=True
    )

    content_type = response.headers.get("Content-Type", "")
    if response.status_code == 200 and "audio/mpeg" in content_type:
        audio_data = BytesIO()
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                audio_data.write(chunk)
        audio_data.seek(0)
        return audio_data.read()

    elif "application/json" in content_type:
        data = response.json()
        for trace in data:
            if trace.get("type") == "text":
                text = trace["payload"]["message"]
                return text
        return None

    else:
        return None

# Convert text to speech using ElevenLabs
# Convert text to speech using ElevenLabs
def convert_text_to_speech(text):
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

        # Generate audio using the correct method
        audio = client.text_to_speech.convert(
            voice_id=VOICE_ID,
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_multilingual_v2"
        )
        
        # Convert audio data to bytes
        audio_data = BytesIO(audio)
        audio_data.seek(0)
        return audio_data.getvalue()
    except Exception as e:
        st.error(f"Text-to-speech conversion failed: {str(e)}")
        return None

# Main app
st.title("Voice AI Assistant")
st.write("Welcome to the Voice AI Assistant! Click the microphone button below to start recording your message.")

# Record and process audio
audio_data = record_audio()
if audio_data:
    with st.spinner("Processing your message..."):
        transcription = transcribe_with_munsit(audio_data)
        if transcription:
            st.write("You said:", transcription)
            
            # Get AI response
            response = interact_with_voiceflow("ايه البيانات الي عندكو عن " + transcription )
            if response:
                st.write("AI response:", response)
                
                # Convert response to speech
                audio_response = convert_text_to_speech(response)
                if audio_response:
                    st.audio(audio_response, format="audio/mp3")
