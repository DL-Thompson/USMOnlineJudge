import os
from judge import app
from judge import config
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['cpp', 'h'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def save(file, filename):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
