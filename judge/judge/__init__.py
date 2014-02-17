# app initialization
from flask import Flask
app = Flask(__name__)


#db session closing
from database import db_session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#db migration
'''
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
migrate = Migrate(app, db_session)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
'''

#secret key
import prod_cfg
app.secret_key = prod_cfg.secret_key


from flask.ext.login import LoginManager
from authomatic import Authomatic
from login_cfg import log_cfg, login_secret_key
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
authomatic = Authomatic(log_cfg, login_secret_key, report_errors=False)


# views initialization
import views
import views_admin