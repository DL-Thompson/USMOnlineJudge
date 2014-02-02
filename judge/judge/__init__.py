from flask import Flask
app = Flask(__name__)

import judge.models


from models import db

db.init_app(app)

import judge.views