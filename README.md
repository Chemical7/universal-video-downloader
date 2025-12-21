# A.see.G - Universal Video Downloader

A modern, elegant web application for downloading videos and audio from any social media platform. Built with FastAPI and vanilla JavaScript, featuring a premium glass-morphism UI.

## ✨ Features

- **Multi-Platform Support**: Download from YouTube, Instagram, X (Twitter), TikTok, and more
- **Format Selection**: Choose from available video qualities and formats
- **Audio Extraction**: Toggle audio-only downloads
- **Orientation Detection**: Automatically detects and displays video orientation (Portrait/Landscape/Square)
- **Direct Downloads**: Browser-native download experience with proper file naming
- **Thumbnail Preview**: See video thumbnails before downloading
- **Premium UI**: Modern glass-morphism design with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Chemical7/universal-video-downloader.git
cd universal-video-downloader
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

4. Open your browser and navigate to:
```
http://localhost:8000
```

## 🎯 Usage

1. **Paste a video URL** from any supported platform into the input field
2. **Click "Find Video"** to fetch available formats
3. **Select your preferred format** from the dropdown
4. **Toggle "Audio Only"** if you only want the audio track
5. **Click "Download Now"** to start the download

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **yt-dlp**: Universal video/audio downloader
- **Requests**: HTTP library for proxying content

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **CSS3**: Glass-morphism effects and animations
- **HTML5**: Semantic markup

## 📁 Project Structure

```
universal-video-downloader/
├── backend/
│   ├── downloader.py      # Video download logic and API endpoints
│   ├── main.py            # FastAPI application entry point
│   ├── requirements.txt   # Python dependencies
│   └── static/
│       ├── index.html     # Main UI
│       ├── script.js      # Frontend logic
│       ├── style.css      # Styling and animations
│       └── favicon.png    # App icon
└── README.md
```

## 🎨 Features in Detail

### Orientation Detection
The app automatically detects video dimensions and displays:
- **Portrait** (📱): For vertical videos (e.g., TikTok, Instagram Reels)
- **Landscape** (🖥️): For horizontal videos (e.g., YouTube)
- **Square** (⬜): For 1:1 aspect ratio videos

### Direct Download Proxy
Instead of opening videos in a new tab, the backend streams content directly to your browser, triggering the native "Save As" dialog with properly formatted filenames.

### Thumbnail Proxy
Bypasses hotlinking protection by proxying thumbnail images through the backend, ensuring they display correctly for all platforms.

## 🚢 Deployment

### Render (Recommended)
1. Fork this repository
2. Create a new Web Service on Render
3. Connect your repository
4. Render will automatically detect the `Procfile` and deploy

### Docker
```bash
cd backend
docker build -t video-downloader .
docker run -p 8000:8000 video-downloader
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This tool is for personal use only. Please respect copyright laws and terms of service of the platforms you download from. Only download content you have the right to download.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful download engine
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Outfit Font](https://fonts.google.com/specimen/Outfit) - Beautiful typography

---

Made with ❤️ by Chemical7
