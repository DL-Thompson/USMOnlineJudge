import os
from judge import app
from database import production_env
import prod_cfg
import dev_cfg
from werkzeug.utils import secure_filename

if production_env:
    UPLOAD_FOLDER = prod_cfg.upload_folder
else:
    UPLOAD_FOLDER = dev_cfg.upload_folder

ALLOWED_EXTENSIONS = set(['cpp', 'h'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def save(file, filename):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
