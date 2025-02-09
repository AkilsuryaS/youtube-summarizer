# VideoGist: AI-Powered YOUTUBE Video Summarizer 🎥✨

VideoGist is a powerful web application that automatically generates concise summaries of YouTube videos, with support for multiple languages. Built with Streamlit and powered by advanced AI, it helps users quickly grasp the key content of any YouTube video.

## 🌟 Features

- **Video Summary Generation**: Get quick, accurate summaries of any YouTube video
- **Multilingual Support**: Summaries available in:
  - English
  - Spanish
  - Tamil
  - Hindi
  - French
- **Recipe Extraction**: Special feature to extract and format recipes from cooking videos
- **Automatic Transcription**: Fallback to audio transcription when subtitles aren't available
- **Interactive UI**: Toggle between summary and full transcription
- **User-Friendly Interface**: Simple, clean design for easy navigation

## 🛠️ Technologies Used

- Python
- Streamlit
- OpenAI API (for transcription)
- Groq API (for summarization)
- yt-dlp (for video processing)

## 🚀 Getting Started

### Prerequisites

```bash
- Python 3.8 or higher
- pip (Python package installer)
```

### Install required packages:
```bash
pip install -r requirements.txt
```

### Set up environment variables:
Create a .env file in the root directory and add your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

### Run the application:
```bash
streamlit run app.py
```

### 📖 How to Use

- Launch the application
- Enter a YouTube video URL
- Select your preferred language for the summary
- Check the "Recipe" box if processing a cooking video
- Click "Summarize" and wait for processing
- Toggle between summary and full transcription as needed

### 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

### 🙏 Acknowledgments

- [OpenAI](https://openai.com/index/whisper/) for providing the transcription API
- [Groq](https://console.groq.com/docs/speech-text) for the powerful summarization API
- [yt-dlp](https://github.com/yt-dlp/yt-dlp/releases) developers for the video processing library
- [Streamlit](https://docs.streamlit.io/) team for the amazing web framework

