import os
import subprocess
from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath('uploads')
OUTPUT_FOLDER = os.path.abspath('converted')
ALLOWED_EXTENSIONS = {'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('word_to_pdf.html')

@app.route('/pdf_converter', methods=['POST'])
def convert_word_to_pdf():
    if 'word_file' not in request.files:
        return jsonify(success=False, error='No file part')

    file = request.files['word_file']

    if file.filename == '':
        return jsonify(success=False, error='No selected file')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        try:
            # Convert DOCX to PDF using LibreOffice headless mode
            result = subprocess.run([
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', app.config['OUTPUT_FOLDER'],
                input_path
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0:
                return jsonify(success=False, error=f"LibreOffice error: {result.stderr.strip()}")

            output_filename = os.path.splitext(filename)[0] + '.pdf'
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

            if not os.path.exists(output_path):
                return jsonify(success=False, error="PDF not generated.")

            return jsonify(success=True, pdf_file=output_filename)

        except FileNotFoundError:
            return jsonify(success=False, error="LibreOffice not installed or not found in PATH.")
        except Exception as e:
            return jsonify(success=False, error=f"Exception occurred: {str(e)}")

    return jsonify(success=False, error='Invalid file type. Only DOCX allowed.')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5005, host='0.0.0.0', debug=True)

