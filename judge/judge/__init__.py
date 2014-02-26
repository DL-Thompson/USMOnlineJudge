# app initialization
from flask import Flask
from judge import config
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from authomatic import Authomatic


#initialize the flask app
app = Flask(__name__)
app.config.from_object('judge.config')
app.secret_key = config.secret_key


#initialize the database
db = SQLAlchemy(app)


#initialize the login manager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
authomatic = Authomatic(config.log_cfg, config.login_secret_key, report_errors=False)


#include the views for the server
import views
