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


@app.route('/login')
def login():
    #displays the login links
    text = db_queries.get_page_content('login')
    return render_template("login.html", text=text)


@app.route('/log/<provider_name>/', methods=['GET', 'POST'])
def log(provider_name):
    #function to actually login the user with oauth requests
    if g.user is not None and g.user.is_authenticated():
        #check to see if the user is already logged in
        return redirect(url_for('login'))

    #get the result from the oauth provider
    response = make_response()
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)

    if result:
        #a result was returned from the oauth provider
        if result.user:
            result.user.update()

        if result.user.email is None or result.user.email == "":
            #An error occured, produce error message to user
            return redirect(url_for('login'))

        #at this point, the user oauth information should be valid
        #check the database to see if it is an existing user
        user = db_queries.get_user(result.user.email)
        if user is None:
            #user was not in the database, a new entry will be registered for them
            first_name = result.user.first_name
            last_name = result.user.last_name
            email = result.user.email
            user = db_posts.add_user(email, first_name, last_name)

        #user is valid, log the user in
        login_user(user, remember=False)
        return redirect(request.args.get('next') or url_for('index'))

    #if it is the first call, return the reponse
    #user info is handled on the second call
    return response


@lm.user_loader
def load_user(email):
    return db_queries.get_user(email)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/statistics')
@login_required
def statistics():
    text = db_queries.get_page_content('statistics')
    return render_template("statistics.html", text=text)


@app.route('/profile')
@login_required
def profile():
    text = db_queries.get_page_content('profile')
    return render_template("profile.html", text=text)
