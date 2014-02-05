# app initialization
from flask import Flask
app = Flask(__name__)

# views initialization
import views

#db session closing
from database import db_session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


#secret key
import prod_cfg
app.secret_key = prod_cfg.secret_key