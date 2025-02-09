import yt_dlp
import os

def extract_audio(youtube_url, output_audio_path="audio.mp3"):
    """
    Extract audio from a YouTube video using yt-dlp and save it as an MP3 file.
    """
    try:
        # Download the audio using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_audio_path.replace(".mp3", ".%(ext)s"),  # Temporary file name
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        return output_audio_path
    except Exception as e:
        raise Exception(f"Error extracting audio: {e}")