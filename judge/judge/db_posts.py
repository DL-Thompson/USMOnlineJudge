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


def add_user(email, first_name, last_name):
    user = models.User(email=email, first_name=first_name, last_name=last_name)
    db_session.add(user)
    db_session.commit()
    return user