from judge import app
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
import app_cache
import forms
import models
import db_queries
import db_posts
from judge import db

USER_PERMISSIONS = 'admin'
BAD_HTML = 'no_permissions.html'

@app.route('/admin')
def admin():
    if USER_PERMISSIONS is 'admin':
        return render_template('/admin/admin_main.html')
    return render_template(BAD_HTML)


@app.route('/admin/page-find')
def db_admin_page():
    if USER_PERMISSIONS is 'admin':
        page_list = db_queries.get_pages()
        return render_template('/admin/admin_page_list.html', pages=page_list)
    return render_template(BAD_HTML)


@app.route('/admin/page-edit/<pg_id>', methods=['GET', 'POST'])
def db_edit_page(pg_id=None):
    msg = request.args.get('msg')
    if USER_PERMISSIONS is 'admin':
        form = forms.DBPageUploadForm(request.form)
        if request.method == 'GET':
            pre_data = db_queries.get_page(pg_id)
            form.title.data = pre_data.page
            form.content.data = pre_data.content
            return render_template('/admin/admin_page_edit.html', form=form, msg=msg)
        else:
            # update the db with the new results
            pg = models.PageContent(form.title.data, form.content.data)
            db_posts.add_page(pg)
            return redirect(url_for('db_edit_page', pg_id=pg_id, msg='Page Updated'))
    return render_template(BAD_HTML)


@app.route('/admin/exercise')
def db_admin_exercise():
    if USER_PERMISSIONS is 'admin':
        return render_template('/admin/admin_exercise_choice.html')
    return render_template(BAD_HTML)


@app.route('/admin/exercise-find')
def db_find_exercise():
    if USER_PERMISSIONS is 'admin':
        exercise_list = db_queries.get_exercise_list()
        return render_template('/admin/admin_exercise_list.html', exercises=exercise_list)
    return render_template(BAD_HTML)


@app.route('/admin/exercise-edit/<ex_id>', methods=['GET', 'POST'])
def db_edit_exercise(ex_id=None):
    msg = request.args.get('msg')
    if USER_PERMISSIONS is 'admin':
        form = forms.DBExerciseUploadForm(request.form)
        if request.method == 'GET':
            pre_data = db_queries.get_exercise(ex_id)
            form.title.data = pre_data.title
            form.category.data = pre_data.category
            form.difficulty.data = pre_data.difficulty
            form.content.data = pre_data.content
            return render_template('/admin/admin_exercise_edit.html', form=form, msg=msg)
        else:
            # update the db with the new results
            exercise = models.Exercises(form.title.data, form.difficulty.data, form.category.data, form.content.data)
            db_posts.add_exercise(exercise)
            return redirect(url_for('db_edit_exercise', ex_id=ex_id, msg='Exercise Updated'))
    return render_template(BAD_HTML)


@app.route('/admin/exercise-add', methods=['GET', 'POST'])
def db_add_exercise():
    if USER_PERMISSIONS is 'admin':
        form = forms.DBExerciseUploadForm(request.form)
        if request.method == 'POST' and form.validate():
            exercise = models.Exercises(form.title.data, form.difficulty.data, form.category.data, form.content.data)
            db.session.add(exercise)
            db.session.commit()
            app_cache.reset_exercise_list()
            return redirect(url_for('db_add_exercise'))
        return render_template('/admin/admin_exercise_add.html', form=form)
    return render_template(BAD_HTML)