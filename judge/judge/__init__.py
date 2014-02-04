# app initialization
from flask import Flask
app = Flask(__name__)

# db initialization
import judge.models
from models import db
db.init_app(app)
'''
# cache initialization
from flask.ext.cache import Cache
cache = Cache(app)
'''
# views initialization
import judge.views