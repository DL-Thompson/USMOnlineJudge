from judge import app
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)
	
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/exercises')
def exercises():
    return render_template("exercises.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/statistics')
def statistics():
    return render_template("statistics.html")