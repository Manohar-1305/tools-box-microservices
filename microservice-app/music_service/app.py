from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
import pygame
from threading import Thread

app = Flask(__name__)

UPLOAD_FOLDER = 'music_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize pygame for server-side playback (not needed for browser playback)
pygame.init()
pygame.mixer.init()

playing_thread = None
current_music = None

@app.route('/')
def home():
    return render_template('music_player.html')

@app.route('/music')
def music_home():
    return render_template('music.html')  # or however it's defined

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('music')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return jsonify({'filename': filename})

@app.route('/list')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

@app.route('/music_files/<filename>')
def serve_music(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/play', methods=['POST'])
def play_music():
    global playing_thread, current_music

    music_file = request.files.get('music')
    if not music_file:
        return jsonify({'error': 'No file provided'}), 400

    filename = secure_filename(music_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    music_file.save(filepath)

    def play(filepath):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
        except Exception as e:
            print("Playback error:", e)

    if not pygame.mixer.music.get_busy():
        playing_thread = Thread(target=play, args=(filepath,))
        playing_thread.start()
        current_music = filepath
        return jsonify({'message': f'Playing {filename}'})
    else:
        return jsonify({'message': 'Another track is already playing'})

@app.route('/stop', methods=['POST'])
def stop_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        return jsonify({'message': 'Music stopped'})
    return jsonify({'message': 'No music is playing'})

if __name__ == '__main__':
    app.run(port=5004, debug=True)
