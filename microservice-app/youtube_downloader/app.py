from flask import Flask, request, send_file, render_template, jsonify
from yt_dlp import YoutubeDL
import os
import uuid

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/youtube')
def youtube_home():
    return render_template('youtube.html')  # or however you're serving the UI

@app.route('/')
def index():
    return render_template('youtube.html')


@app.route('/fetch_playlist')
def fetch_playlist():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        videos = []
        if 'entries' in info:  # It's a playlist
            for entry in info['entries']:
                if entry:
                    videos.append({
                        "title": entry.get("title", "No title"),
                        "url": f"https://www.youtube.com/watch?v={entry.get('id')}"
                    })
        else:  # Single video
            videos.append({
                "title": info.get("title", "No title"),
                "url": url
            })

        return jsonify({"videos": videos})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch videos: {str(e)}"}), 500


@app.route('/download_best')
def download_best():
    url = request.args.get('url')
    if not url:
        return "Missing URL parameter", 400

    unique_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_DIR, f"{unique_id}.%(ext)s")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_template,
        'quiet': True,
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "video")

        for ext in ['mp4', 'mkv', 'webm']:
            path = os.path.join(DOWNLOAD_DIR, f"{unique_id}.{ext}")
            if os.path.exists(path):
                return send_file(
                    path,
                    as_attachment=True,
                    download_name=f"{title}.{ext}",
                    mimetype="video/mp4"
                )

        return "Download failed or file not found", 500
    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(port=5002, debug=True)
