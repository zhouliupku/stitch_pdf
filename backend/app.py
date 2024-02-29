from flask import Flask, request, redirect, send_file, jsonify
from flask_cors import CORS
import PyPDF2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
MERGED_FOLDER = 'merged'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MERGED_FOLDER'] = MERGED_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def merge_pdfs(pdf_files, output_file):
    merger = PyPDF2.PdfMerger()

    for pdf_file in pdf_files:
        merger.append(pdf_file)

    with open(output_file, 'wb') as output:
        merger.write(output)

    merger.close()


@app.route('/')
def index():
    return "Hello World"


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files were uploaded'}), 400

        files = request.files.getlist('files[]')
        uploaded_files = []

        for file in files:
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                uploaded_files.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        merged_filename = 'merged.pdf'
        merge_pdfs(uploaded_files, os.path.join(app.config['MERGED_FOLDER'], merged_filename))

        return redirect('/api/download')


@app.route('/api/download')
def download_file():
    merged_filename = 'merged.pdf'
    return send_file(os.path.join(app.config['MERGED_FOLDER'], merged_filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
