from judge import app, lm, authomatic
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import db_queries
import upload
import views_admin
import views_login
import file_handling


#imports for login
from flask import g, make_response, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from authomatic.adapters import WerkzeugAdapter
import db_posts


#imports for profile
from forms import ProfileForm
from app_cache import is_profile_changed
from forms import SearchForm
from models import Profile


@app.route('/')
@app.route('/index')
def index():
    text = db_queries.get_page_content('index')
    return render_template("index.html", text=text)


@app.route('/exercises')
def exercises():
    text = db_queries.get_page_content('exercises')
    exercise_list = db_queries.get_exercise_list()
    return render_template("exercises.html", text=text, leftPanelContent=exercise_list)


@app.route('/exercise/<ex_id>', methods=['GET', 'POST'])
@login_required
def display_exercise(ex_id=None):
    if request.method == 'POST':
        profile = db_queries.get_profile(current_user.primary_email)
        user_id = profile.user_id
        file = request.files['file']
        if file:
            data = file.read()
            exercise = db_queries.get_exercise(ex_id)
            return render_template("exercise.html", exercise=exercise, data=data)
        else:
            text = request.form['code_editor']
            if text:
                filename = str(ex_id) + "-" + str(user_id) + ".cpp"
                file_handling.save(text, filename)
                session['fn'] = filename
                return redirect(url_for('display_results', ex_id=ex_id))
    exercise = db_queries.get_exercise(ex_id)
    exercise_list = db_queries.get_exercise_list()
    return render_template("exercise.html", exercise=exercise, leftPanelContent=exercise_list)


@app.route('/exercise/<ex_id>/results')
@login_required
def display_results(ex_id=None):
    filename = session['fn']
    results = file_handling.get_results(filename)
    #if success, the results contain valid data, assign it
    if file_handling.SUCCESS_MESSAGE in results.values():
        print "Success in results."
        time = results['time']
        memory = results['memory']
        passed = True
    else:
        #if error or fail, there is no data, set incorrect values
        time = None
        memory = None
        passed = False
    if ex_id:
        #post the statistic to the database if the exercise number is valid
        db_posts.add_exercise_statistic(current_user.primary_email, ex_id, time, memory, passed)
    session.pop('fn', None)
    #builds a list of messages to pass to the template
    list = []
    list.append(results['message'])
    if file_handling.SUCCESS_MESSAGE in results.values():
        list.append("Your program took " + str(time) + " seconds to complete.")
    elif file_handling.INCORRECT_MESSAGE in results.values():
        pass
    else:
        list.append(results['errors'])
    return render_template("submit_result.html", results=list)


@app.before_request
def before_request():
    #if a user is logged in, it is set in the global variable so the login function
    #won't be executed when not needed
    g.user = current_user
    g.search_form = SearchForm()


@app.route('/statistics')
@login_required
def statistics():
    text = db_queries.get_page_content('statistics')
    statistics = db_queries.get_users_statistics(current_user.primary_email, None)

    #get user id to pass to the template to build the link to the last correctly submitted exercise
    user_id = db_queries.get_user(current_user.primary_email).user_id
    link_dir = app.config['STORAGE_FOLDER']
    return render_template("statistics.html", text=text, statistics=statistics, link_dir=link_dir, user_id=user_id)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    text = db_queries.get_page_content('profile')
    if request.method == 'POST':
        #if the submit button was hit, loads the information into the form
        form = ProfileForm(request.form)
        if form.validate():
            #sends the user to the profile/edit profile page with updated information
            # if is_profile_changed(form):
            #     #user profile has been changed, update the database
            db_posts.update_profile(form, current_user.primary_email)
            text = db_queries.get_page_content('profile')
            profile = db_queries.get_profile(current_user.primary_email)
            return render_template("my_profile.html", text=text, profile=profile, form=form, leftProfileContent=profile)
        else:
            profile = db_queries.get_profile(current_user.primary_email)
            return render_template("my_profile.html", text=text, profile=profile, form=form, leftProfileContent=profile)

    #sends the user to the profile/edit profile page for GET methods
    profile = db_queries.get_profile(current_user.primary_email)
    form = ProfileForm(obj=profile)
    return render_template("my_profile.html", text=text, profile=profile, form=form, leftProfileContent=profile)


@app.route('/display_profile/<profile_id>')
def display_profile(profile_id):
    profile = db_queries.get_profile_from_id(profile_id)
    statistics = db_queries.get_users_statistics(None, profile_id)
    return render_template('view_profile.html', profile=profile, statistics=statistics)


@app.route('/delete_profile')
@login_required
def delete_profile():
    db_posts.delete_user(current_user.primary_email)
    return redirect(url_for('logout'))


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm(request.form)
    if form.validate():
        return redirect(url_for('search_result', query=form.search.data))
    return redirect(url_for('index'))


@app.route('/search_result/<query>')
def search_result(query):
    #returns the search results for a users searched profile
    results = Profile.query.whoosh_search(query, 50).filter(Profile.show_public == True).all()
    return render_template('search_results.html', query=query, results=results)

#route to serve the saved source code files
@app.route('/source_code/<path:filename>')
def source_code(filename):
    path = app.config['STORAGE_FOLDER']
    from flask import send_from_directory
    return send_from_directory(path, filename)