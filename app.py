import subprocess
import sys
import os

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, Response
from Master import processSheets
import config

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.debug = True

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS  # PyInstaller temp directory
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define folder paths relative to the base directory
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ERROR_FILES_FOLDER = os.path.join(BASE_DIR, 'error_logs')
DOWNLOAD_TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'downloadTemplates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ERROR_FILES_FOLDER'] = ERROR_FILES_FOLDER
app.config['DOWNLOAD_TEMPLATES_FOLDER'] = DOWNLOAD_TEMPLATES_FOLDER
ALLOWED_EXTENSIONS = {'xlsx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(ERROR_FILES_FOLDER):
    os.makedirs(ERROR_FILES_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('File Not attached!', "error")
        return redirect(request.url)
    
    file = request.files['file']
    config.url = request.form['base_url']
    url = request.form['base_url']
    # type = request.form['type']
    # username = request.form['username']
    # password = request.form['password']
    # mode = request.form.get('chkmode')

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        error_files = processSheets(filename, app.config['ERROR_FILES_FOLDER'], url)
        
        if error_files:
            # error_files = [f[0].rsplit("\\", 1)[-1] for f in error_files]
            # error_files = os.path.basename(f[0] for f in error_files)
            error_files = error_files.split("\\")[-1]
            return jsonify({'error_files': error_files})
        else:
            return jsonify({'message': 'No Records Saved'})
    else:
        flash('Allowed file types are .xlsx', 'error')
        return redirect(request.url)


@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(app.config['ERROR_FILES_FOLDER'], filename)
    return send_file(path, as_attachment=True)

@app.route('/downloadTemplates/<filename>')
def download_template(filename):
    path = os.path.join(app.config['DOWNLOAD_TEMPLATES_FOLDER'], filename)
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app)
