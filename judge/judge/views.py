from judge import app
from flask import render_template
import models


@app.route('/')
@app.route('/index')
def index():
    text = models.PageContent.query.filter_by(page='index').first().get_content()
    if not text:
        text = "DEBUG, ERROR: DB miss"
    return render_template("index.html", text=text)


@app.route('/exercises')
def exercises():
    text = models.PageContent.query.filter_by(page='exercises').first().get_content()
    if not text:
        text = "DEBUG, ERROR: DB miss"
    return render_template("exercises.html", text=text)


@app.route('/profile')
def profile():
    text = models.PageContent.query.filter_by(page='profile').first().get_content()
    if not text:
        text = "DEBUG, ERROR: DB miss"
    return render_template("profile.html", text=text)


@app.route('/login')
def login():
    text = models.PageContent.query.filter_by(page='login').first().get_content()
    if not text:
        text = "DEBUG, ERROR: DB miss"
    return render_template("login.html", text=text)


@app.route('/statistics')
def statistics():
    text = models.PageContent.query.filter_by(page='statistics').first().get_content()
    if not text:
        text = "DEBUG, ERROR: DB miss"
    return render_template("statistics.html", text=text)
