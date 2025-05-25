# Voice AI Assistant

A Streamlit web application that provides voice interaction capabilities using ElevenLabs for text-to-speech and Voiceflow for conversation flow.

## Features

- Real-time voice recording
- Speech-to-text transcription using Munsit
- Natural conversation flow using Voiceflow
- High-quality text-to-speech using ElevenLabs

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application locally:
```bash
streamlit run app.py
```

## Deployment

This application can be deployed on Streamlit Community Cloud:

1. Fork this repository to your GitHub account
2. Sign up for [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Deploy the app by connecting your GitHub repository

## Environment Variables

The following API keys are required:

- MUNSIT_API_KEY
- VOICEFLOW_API_KEY
- ELEVENLABS_API_KEY

Add these to your Streamlit secrets when deploying.