import app_cache
from app_cache import KEY_PROFILE
from judge import models
from judge import db
import db_queries



def add_exercise(exercise):
    ex = models.Exercises.query.filter_by(title=exercise.title).first()
    if ex:
        ex.category = exercise.title
        ex.difficulty = exercise.difficulty
        ex.content = exercise.content
        db.session.commit()
    else:
        db.session.add(exercise)
        db.session.commit()
    app_cache.reset_exercise_list()
    app_cache.reset_exercise(ex.id)


def add_page(p):
    pg = models.PageContent.query.filter_by(page=p.page).first()
    if pg:
        pg.page = p.page
        pg.content = p.content
        db.session.commit()
    else:
        db.session.add(p)
        db.session.commit()
    app_cache.reset_page_list()
    app_cache.reset_page(pg.id)


def add_user(primary_email):
    #creates a new user with a blank profile
    user = models.User(primary_email=primary_email)
    db.session.add(user)
    db.session.commit()
    profile = models.Profile(user)
    db.session.add(profile)
    db.session.commit()
    return user


def update_profile(profile_form, primary_email):
    #clears the profile from cache so the new profile will be queried
    app_cache.cache.set(KEY_PROFILE, None)

    #gets the user, gets their profile, and updates the fields
    user = models.User.query.filter_by(primary_email=primary_email).first()
    profile =  models.Profile.query.get(user.user_id)
    profile.show_public = profile_form.show_public.data
    profile.full_name = profile_form.full_name.data
    profile.public_email = profile_form.public_email.data
    if profile_form.homepage.data == "":
        profile.homepage = profile_form.homepage.data
    elif "http://" not in profile_form.homepage.data:
        profile.homepage = "http://" + profile_form.homepage.data
    else:
        profile.homepage = profile_form.homepage.data
    profile.company = profile_form.company.data
    profile.school = profile_form.school.data
    profile.location = profile_form.location.data
    db.session.commit()


def delete_user(primary_email):
    #deletes a user and their profile
    user =  db_queries.get_user(primary_email)
    #does not use the get_profile query to be sure it's the actual db
    #profile, and not the one stored in cache
    profile = models.Profile.query.get(user.user_id)
    db.session.delete(profile)
    db.session.delete(user)
    db.session.commit()
