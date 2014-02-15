import app_cache
import models
from database import db_session


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

