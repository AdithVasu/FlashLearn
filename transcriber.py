import os
import tempfile
import yt_dlp
import httpx
import streamlit as st

@st.cache_data(show_spinner="Downloading and transcribing audio...")
def transcribe_youtube_video(youtube_url: str):
    """
    Downloads the audio from a YouTube video and transcribes it using the Deepgram API directly.
    
    Args:
        youtube_url (str): The URL of the YouTube video.

    Returns:
        str: The full transcribed text.
    """
    try:
       
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, 'audio.mp4')
            
            
            ydl_opts = {
                'format': 'm4a/bestaudio/best',
                'outtmpl': temp_file_path,
                'noplaylist': True,
                'verbose': False
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            
            
            with open(temp_file_path, "rb") as audio_file:
                audio_data = audio_file.read()

            
            url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&punctuate=true&diarize=true"
            headers = {
                "Authorization": f"Token {st.secrets['DEEPGRAM_API_KEY']}",
                "Content-Type": "audio/mp4"
            }
            
            
            with httpx.Client(timeout=60.0) as client:
                response = client.post(url, headers=headers, content=audio_data)
                response.raise_for_status()  

            response_json = response.json()
            
            transcript = response_json['results']['channels'][0]['alternatives'][0]['transcript']
            
            return transcript

    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None