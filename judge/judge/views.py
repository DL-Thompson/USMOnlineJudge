from judge import app
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import models
import queries
import forms
from database import db_session


@app.route('/db-add-exercise', methods=['GET', 'POST'])
def db_add_exercise():
    form = forms.DBExerciseUploadForm(request.form)
    if request.method == 'POST' and form.validate():
        exercise = models.Exercises(form.title.data, form.difficulty.data, form.category.data, form.content.data)
        db_session.add(exercise)
        db_session.commit()
        return redirect(url_for('db_add_exercise'))
    return render_template('_db_add_exercises.html', form=form)


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
