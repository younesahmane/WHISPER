
# YouTube Whisper Transcription API

This repository provides a simple Flask-based API to download YouTube audio and transcribe it using OpenAI’s Whisper model.

## Prerequisites

1. **Python 3.8+**  
2. **FFmpeg**  
   - **Ubuntu/Debian**:  
     ```bash
     sudo apt update
     sudo apt install -y ffmpeg
     ```
   - **macOS (Homebrew)**:  
     ```bash
     brew install ffmpeg
     ```
   - **Windows**:  
     Download from [ffmpeg.org](https://ffmpeg.org/) and add to your PATH.

## Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/yt-whisper-api.git
   cd yt-whisper-api
````

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**

   * **Linux/macOS**:

     ```bash
     source venv/bin/activate
     ```
   * **Windows (PowerShell)**:

     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **Windows (CMD)**:

     ```cmd
     .\venv\Scripts\activate.bat
     ```

4. **Upgrade `pip`**

   ```bash
   pip install --upgrade pip
   ```

5. **Install dependencies**
   First, create a `requirements.txt` with the following contents:

   ```
   openai-whisper
   Flask>=2.0
   Flask-Cors>=3.0
   yt-dlp>=2023.12.1
   
   git+https://github.com/openai/whisper.git
   ```

   Then install:

   ```bash
   pip install -r requirements.txt
   ```

## Running the API

With the virtual environment activated and dependencies installed:

```bash
flask --app test run --port 5001
```

You should see:

```
🚀 Flask API running on port 5001
   POST http://localhost:5001/transcribe  {"url":"<YouTube-link>"}
```


