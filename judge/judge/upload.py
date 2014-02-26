import os
from judge import app
from judge import config
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = config.upload_folder


ALLOWED_EXTENSIONS = set(['cpp', 'h'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def save(file, filename):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
