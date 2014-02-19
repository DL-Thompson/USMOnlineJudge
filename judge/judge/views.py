from judge import app, lm, authomatic
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import db_queries
import upload

#imports for login
from flask import g, make_response, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from authomatic.adapters import WerkzeugAdapter
import db_posts


#imports for profile
from forms import ProfileForm
from app_cache import is_profile_changed

@app.route('/')
@app.route('/index')
def index():
    text = db_queries.get_page_content('index')
    return render_template("index.html", text=text)


@app.route('/exercises')
def exercises():
    text = db_queries.get_page_content('exercises')
    exercise_list = db_queries.get_exercise_list()
    return render_template("exercises.html", text=text, exercises=exercise_list)


@app.route('/exercise/<ex_id>', methods=['GET', 'POST'])
def display_exercise(ex_id=None):
    if request.method == 'POST':
        file = request.files['file']
        if file and upload.allowed_file(file.filename):
            filename = upload.secure_filename(file.filename)
            upload.save(file, filename)
            return redirect(url_for('display_exercise', ex_id=ex_id))
    exercise = db_queries.get_exercise(ex_id)
    return render_template("exercise.html", exercise=exercise)


@app.before_request
def before_request():
    #if a user is logged in, it is set in the global variable so the login function
    #won't be executed when not needed
    g.user = current_user


@app.route('/statistics')
@login_required
def statistics():
    text = db_queries.get_page_content('statistics')
    return render_template("statistics.html", text=text)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    text = db_queries.get_page_content('profile')
    if request.method == 'POST':
        #if the submit button was hit, loads the information into the form
        form = ProfileForm(request.form)
        if form.validate():
            #sends the user to the profile/edit profile page with updated information
            if is_profile_changed(form):
                #user profile has been changed, update the database
                db_posts.update_profile(form, current_user.primary_email)
            text = db_queries.get_page_content('profile')
            profile = db_queries.get_profile(current_user.primary_email)
            return render_template("profile.html", text=text, profile=profile, form=form)
        else:
            profile = db_queries.get_profile(current_user.primary_email)
            return render_template("profile.html", text=text, profile=profile, form=form)

    #sends the user to the profile/edit profile page for GET methods
    profile = db_queries.get_profile(current_user.primary_email)
    form = ProfileForm(obj=profile)
    return render_template("profile.html", text=text, profile=profile, form=form)
