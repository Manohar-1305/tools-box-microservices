import os
import requests
from flask import Flask, request, render_template, jsonify, send_file, redirect, Response
import config
from io import BytesIO

app = Flask(__name__, static_folder=None)

PDF_SERVICE = config.PDF_SERVICE
YTDL_SERVICE = config.YTDL_SERVICE
AUDIO_SERVICE = config.AUDIO_SERVICE
MUSIC_SERVICE = config.MUSIC_SERVICE
WORD2PDF_SERVICE = config.WORD2PDF_SERVICE

# ---------------- UI Routes ---------------- #

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pdf_converter')
def pdf_converter_ui():
    return redirect(f'{PDF_SERVICE}/pdf_converter', code=302)

@app.route('/word_to_pdf', methods=['GET'])
def word_to_pdf_ui():
    return redirect(f'{WORD2PDF_SERVICE}/', code=302)


@app.route('/youtube')
def youtube_ui():
    return redirect(f'{YTDL_SERVICE}/youtube', code=302)

from flask import Response  # Don't forget this import

@app.route('/convert')
def convert_ui():
    try:
        resp = requests.get(f'{AUDIO_SERVICE}/convert')
        return Response(
            resp.content,
            status=resp.status_code,
            content_type=resp.headers.get('Content-Type', 'text/html')
        )
    except requests.exceptions.RequestException as e:
        return Response(f"Error contacting audio service: {str(e)}", status=500)

# ✅ This will proxy static files like /static/text_to_audio.css
@app.route('/static/<path:filename>', endpoint='static')
def proxy_static_from_audio(filename):
    try:
        resp = requests.get(f'{AUDIO_SERVICE}/static/{filename}')
        return Response(
            resp.content,
            status=resp.status_code,
            content_type=resp.headers.get('Content-Type', 'application/octet-stream')
        )
    except requests.exceptions.RequestException as e:
        return Response(f"Static file error: {str(e)}", status=500)

@app.route('/music')
def music_ui():
    return redirect(f'{MUSIC_SERVICE}/music', code=302)

# ---------------- API Routes ---------------- #

@app.route('/api/pdf', methods=['POST'])
def convert_pdf():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    try:
        response = requests.post(f'{PDF_SERVICE}/convert', files={'file': file})
        return send_file(
            BytesIO(response.content),
            as_attachment=True,
            download_name=f"{file.filename.rsplit('.', 1)[0]}.docx",
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'PDF service unavailable', 'details': str(e)}), 503

@app.route('/api/pdf/download/<filename>')
def download_pdf_file(filename):
    try:
        response = requests.get(f'{PDF_SERVICE}/download/{filename}', stream=True)
        temp_path = os.path.join("temp_files", filename)
        os.makedirs("temp_files", exist_ok=True)
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return send_file(temp_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': 'Download failed', 'details': str(e)}), 500

@app.route('/api/youtube/info', methods=['GET'])
def get_playlist_info():
    try:
        url = request.args.get('url')
        response = requests.get(f'{YTDL_SERVICE}/playlist_info', params={'url': url})
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'YouTube service unavailable', 'details': str(e)}), 503

@app.route('/api/youtube/download', methods=['GET'])
def download_video():
    try:
        url = request.args.get('url')
        itag = request.args.get('itag')
        response = requests.get(
            f'{YTDL_SERVICE}/download_video',
            params={'url': url, 'itag': itag},
            stream=True
        )
        return send_file(BytesIO(response.content), as_attachment=True, download_name="video.mp4", mimetype='video/mp4')
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Download failed', 'details': str(e)}), 503

@app.route('/api/audio/convert', methods=['POST'])
def convert_text_to_audio():
    try:
        text = request.form.get('text')
        response = requests.post(f'{AUDIO_SERVICE}/convert', data={'text': text})
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Audio service unavailable', 'details': str(e)}), 503

@app.route('/api/music/play', methods=['POST'])
def play_music():
    try:
        file = request.files.get('music')
        if not file:
            return jsonify({'error': 'No file uploaded'}), 400
        response = requests.post(f'{MUSIC_SERVICE}/play', files={'music': file})
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Music service unavailable', 'details': str(e)}), 503

@app.route('/api/music/stop', methods=['POST'])
def stop_music():
    try:
        response = requests.post(f'{MUSIC_SERVICE}/stop')
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Music service unavailable', 'details': str(e)}), 503

@app.route('/api/word_to_pdf', methods=['POST'])
def convert_wordtopdf():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    try:
        response = requests.post(f'{WORD2PDF_SERVICE}/convert', files={'file': file})
        return send_file(
            BytesIO(response.content),
            as_attachment=True,
            download_name=f"{file.filename.rsplit('.', 1)[0]}.pdf",
            mimetype='application/pdf'
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Word2PDF service unavailable', 'details': str(e)}), 503



@app.route('/gateway', methods=['GET'])
def gateway_status():
    return "Gateway is up"

# ---------------- Run ---------------- #
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
