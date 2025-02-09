import os
from dotenv import load_dotenv
import streamlit as st
from utils.transcriber import get_subtitles, transcribe_audio_openai
from utils.summarizer import summarize_text, extract_recipe
import yt_dlp

# Load environment variables from .env file
load_dotenv()

# Access the API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Streamlit app title
st.title("YouTube Video Summarizer")

# Initialize session state variables
if "transcription" not in st.session_state:
    st.session_state.transcription = None
if "recipe" not in st.session_state:
    st.session_state.recipe = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "view" not in st.session_state:
    st.session_state.view = None

# Input YouTube link
youtube_url = st.text_input("Enter the YouTube video link:")

# Language selection for summarization
language = st.selectbox("Select the language for summarization:", ["English", "Tamil", "Hindi", "Spanish", "French"])

# Checkbox to indicate if the video is a cooking recipe
is_recipe = st.checkbox("Is this video a cooking recipe?")

def get_video_info(youtube_url):
    """
    Fetch video title and thumbnail URL using yt-dlp.
    """
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            video_title = info_dict.get("title", "No Title")
            thumbnail_url = info_dict.get("thumbnail", "")
            return video_title, thumbnail_url
    except Exception as e:
        raise Exception(f"Error fetching video info: {e}")

# Display video link, title, and thumbnail
if youtube_url.strip():
    try:
        video_title, thumbnail_url = get_video_info(youtube_url)
        st.subheader("Video Details:")
        st.write(f"**Title:** {video_title}")
        st.write(f"**Link:** {youtube_url}")
        if thumbnail_url:
            st.image(thumbnail_url, caption="Video Thumbnail", width=300)
    except Exception as e:
        st.error(f"Error fetching video details: {e}")

if st.button("Summarize"):
    if not youtube_url.strip():  # Check if the input is empty
        st.error("Please enter a valid YouTube link.")
    else:
        with st.spinner("Checking for subtitles..."):
            try:
                # Initialize progress bar
                progress_bar = st.progress(0)

                # Step 1: Check for subtitles
                subtitles_file = get_subtitles(youtube_url)
                if subtitles_file:
                    st.success("Subtitles found! Translating...")
                    with open(subtitles_file, "r", encoding="utf-8") as f:
                        subtitles = f.read()
                    progress_bar.progress(50)  # Update progress to 50%

                    # Step 2: Translate subtitles to the chosen language
                    with st.spinner("Translating subtitles..."):
                        if is_recipe:
                            # Extract recipe from subtitles
                            st.session_state.recipe = extract_recipe(subtitles, language, GROQ_API_KEY)
                            st.success("Recipe extracted!")
                        else:
                            # Summarize subtitles
                            st.session_state.summary = summarize_text(subtitles, language, GROQ_API_KEY)
                            st.success("Translation completed!")
                    progress_bar.progress(100)  # Update progress to 100%

                    # Store transcription in session state
                    st.session_state.transcription = subtitles

                    # Clean up subtitles file
                    os.remove(subtitles_file)
                else:
                    st.warning("No subtitles found. Extracting audio...")
                    # Step 3: Fallback to audio extraction and transcription
                    with st.spinner("Transcribing audio..."):
                        transcription = transcribe_audio_openai(youtube_url, OPENAI_API_KEY)
                        progress_bar.progress(50)  # Update progress to 50%
                        st.success("Transcription completed!")

                        # Step 4: Translate transcription to the chosen language
                        with st.spinner("Translating transcription..."):
                            if is_recipe:
                                # Extract recipe from transcription
                                st.session_state.recipe = extract_recipe(transcription, language, GROQ_API_KEY)
                                st.success("Recipe extracted!")
                            else:
                                # Summarize transcription
                                translation_prompt = f"Translate the following text to {language}:\n{transcription}"
                                st.session_state.summary = summarize_text(translation_prompt, language, GROQ_API_KEY)
                                st.success("Translation completed!")
                        progress_bar.progress(100)  # Update progress to 100%

                        # Store transcription in session state
                        st.session_state.transcription = transcription

                # Display summary or recipe by default
                if st.session_state.recipe or st.session_state.summary:
                    st.subheader("Summary:" if not is_recipe else "Recipe:")
                    st.write(st.session_state.recipe if is_recipe else st.session_state.summary)

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Add buttons to toggle between summary and transcription
if (st.session_state.transcription and 
    (st.session_state.recipe is not None or st.session_state.summary is not None)):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("View Summary"):
            st.session_state.view = "summary"
    with col2:
        if st.button("View Transcription"):
            st.session_state.view = "transcription"

    # Display content based on the selected view
    if st.session_state.view == "summary":
        st.subheader("Summary:" if not is_recipe else "Recipe:")
        st.write(st.session_state.recipe if is_recipe else st.session_state.summary)
    elif st.session_state.view == "transcription":
        st.subheader("Transcription:")
        st.write(st.session_state.transcription)