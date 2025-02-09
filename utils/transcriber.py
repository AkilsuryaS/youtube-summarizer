from openai import OpenAI
import yt_dlp
import os

def get_subtitles(youtube_url):
    """
    Check if subtitles are available for the YouTube video and extract them.
    """
    try:
        ydl_opts = {
            'writesubtitles': True,  # Enable subtitle extraction
            'subtitlesformat': 'vtt',  # Use VTT format for subtitles
            'skip_download': True,  # Skip downloading the video
            'outtmpl': 'subtitles',  # Save subtitles as subtitles.vtt
            'quiet': True,  # Suppress yt-dlp output
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            if 'subtitles' in info_dict or 'automatic_captions' in info_dict:
                # Download subtitles
                ydl.download([youtube_url])
                # Check if the subtitles file exists
                if os.path.exists("subtitles.vtt"):
                    return "subtitles.vtt"
                else:
                    return None
            else:
                return None
    except Exception as e:
        raise Exception(f"Error checking for subtitles: {e}")

def transcribe_audio_openai(youtube_url, api_key):
    """
    Transcribe audio from a YouTube URL using OpenAI's Whisper API in the original language.
    """
    try:
        # Use yt-dlp to download the audio as an MP3 file
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'audio',  # Save as audio.mp3 (no extension in outtmpl)
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # The downloaded file will be saved as audio.mp3
        audio_file_path = "audio.mp3"

        # Check if the file exists
        if not os.path.exists(audio_file_path):
            raise Exception("Failed to download audio file.")

        # Initialize the OpenAI client
        client = OpenAI(api_key=api_key)

        # Transcribe the audio using OpenAI's Whisper API in the original language
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        # Clean up the audio file after transcription
        os.remove(audio_file_path)

        return transcription.text
    except Exception as e:
        raise Exception(f"Error transcribing audio: {e}")