# -----------------------------------------------------------
# 0.  Dependencies (runs only if missing; comment out later)
# -----------------------------------------------------------
import subprocess, sys, importlib, pkg_resources, json, threading, tempfile, os, shutil
"""
def _ensure(pkgs):
    for p in pkgs:
        try:
            importlib.import_module(p.split("==")[0])
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", p])

_ensure([
    "flask>=3.0.0",
    "pytubefix>=0.2.4",
    "moviepy>=1.0.3",
    "git+https://github.com/openai/whisper.git@v20230314",
])"""

# -----------------------------------------------------------
# 1.  Imports
# -----------------------------------------------------------
from flask import Flask, request, jsonify
from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import VideoFileClip
import whisper

# Whisper model is loaded once at start-up to save time
WHISPER_MODEL = whisper.load_model("medium")

# -----------------------------------------------------------
# 2.  Helper: download video, extract audio, transcribe
# -----------------------------------------------------------
TMP_DIR = tempfile.mkdtemp(prefix="yt-whisper-")

def download_and_transcribe(url: str) -> dict:
    """
    Returns:
        {
          'title': ...,
          'transcript': ...,
          'duration_sec': ...,
        }
    Raises:
        Exception on any failure (caller handles)
    """
    # Download best progressive (audio+video) stream
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.get_highest_resolution()
    video_path = stream.download(output_path=TMP_DIR, filename="video")
    
    # Extract audio ➔ mp3 (moviepy needs ffmpeg available)
    clip = VideoFileClip(video_path)
    audio_path = os.path.join(TMP_DIR, "audio.mp3")
    clip.audio.write_audiofile(audio_path, logger=None)
    clip.close()
    
    # Transcribe with Whisper-turbo
    result = WHISPER_MODEL.transcribe(audio_path)
    
    # Clean up large video to save space
    try:
        os.remove(video_path)
    except OSError:
        pass
    
    return {
        "title": yt.title,
        "transcript": result["text"],
        "duration_sec": int(yt.length),
    }
                                                                                                                                                
# -----------------------------------------------------------
# 3.  Flask app
# -----------------------------------------------------------
def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        return {
            "message": "POST a JSON body {\"url\": \"<YouTube-link>\"} to /transcribe"
        }

    @app.route("/transcribe", methods=["POST"])
    def transcribe_route():
        data = request.get_json(silent=True) or {}
        url  = data.get("url")
        if not url:
            return jsonify(error="Request JSON must contain a 'url' field"), 400
        try:
            payload = download_and_transcribe(url)
            return jsonify(payload)
        except Exception as e:
            # In production you would log the traceback
            return jsonify(error=str(e)), 500

    return app


app = create_app()

# -----------------------------------------------------------
# 4.  Launch server in a background thread
# -----------------------------------------------------------
def _run():
    # host='0.0.0.0' ➔ bind on all interfaces so it’s visible outside
    # debug=False avoids Werkzeug reloader spawning extra processes (simpler in notebooks)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)

threading.Thread(target=_run, daemon=True).start()

print(
    "🎉  Flask API is now running!\n"
    "   ➜ POST   http://<node-IP>:5000/transcribe   {\"url\": \"<YouTube-link>\"}"
)
