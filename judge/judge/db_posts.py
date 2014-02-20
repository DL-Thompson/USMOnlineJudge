import app_cache
from app_cache import KEY_PROFILE
import models
from database import db_session
import db_queries


def add_exercise(exercise):
    ex = models.Exercises.query.filter_by(title=exercise.title).first()
    if ex:
        ex.category = exercise.title
        ex.difficulty = exercise.difficulty
        ex.content = exercise.content
        db_session.commit()
    else:
        db_session.add(exercise)
        db_session.commit()
    app_cache.reset_exercise_list()
    app_cache.reset_exercise(ex.id)


def add_page(p):
    pg = models.PageContent.query.filter_by(page=p.page).first()
    if pg:
        pg.page = p.page
        pg.content = p.content
        db_session.commit()
    else:
        db_session.add(p)
        db_session.commit()
    app_cache.reset_page_list()
    app_cache.reset_page(pg.id)


def add_user(primary_email):
    #creates a new user with a blank profile
    user = models.User(primary_email=primary_email)
    db_session.add(user)
    db_session.commit()
    profile = models.Profile(user)
    db_session.add(profile)
    db_session.commit()
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
    db_session.commit()

