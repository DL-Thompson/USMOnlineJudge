from judge import app
from flask import render_template
import models
import queries


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template("hello.html", name=name)


@app.route('/')
@app.route('/index')
def index():
    text = queries.get_page_content('index')
    return render_template("index.html", text=text)


@app.route('/exercises')
def exercises():
    text = queries.get_page_content('exercises')
    return render_template("exercises.html", text=text)


@app.route('/profile')
def profile():
    text = queries.get_page_content('profile')
    return render_template("profile.html", text=text)


@app.route('/login')
def login():
    text = queries.get_page_content('login')
    return render_template("login.html", text=text)


@app.route('/statistics')
def statistics():
    text = queries.get_page_content('statistics')
    return render_template("statistics.html", text=text)
