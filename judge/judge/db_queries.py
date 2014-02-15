import models
from app_cache import cache, TIMEOUT, ERROR_DB_MSG, KEY_PAGE, KEY_PAGES, KEY_EXERCISE, KEY_EXERCISES


def get_page_content(page_title):
    key = '%s%s' % (KEY_PAGE, page_title)
    val = cache.get(key)
    print 'querying', key, val
    if val is None:
        val = models.PageContent.query.filter_by(page=page_title).first().get_content()
        if val is None:
            val = ERROR_DB_MSG
        cache.set(key, val, timeout=TIMEOUT)
    return val


def get_page(pg_id):
    key = '%s%s' % (KEY_PAGE, pg_id)
    val = cache.get(key)
    if val is None:
        val = models.PageContent.query.filter_by(id=pg_id).first()
        if val is None:
            val = ERROR_DB_MSG
        cache.set(key, val, timeout=TIMEOUT)
    return val


def get_pages():
    key = KEY_PAGES
    val = cache.get(key)
    if val is None:
        val = models.PageContent.query.all()
        if val is None:
            val = ERROR_DB_MSG
        cache.set(key, val, timeout=TIMEOUT)
    return val


def get_exercise_list():
    key = KEY_EXERCISES
    val = cache.get(key)
    if val is None:
        val = models.Exercises.query.all()
        if val is None:
            val = ERROR_DB_MSG
        cache.set(key, val, timeout=TIMEOUT)
    return val


def get_exercise(ex_id):
    key = '%s%s' % (KEY_EXERCISE, ex_id)
    val = cache.get(key)
    if val is None:
        val = models.Exercises.query.filter_by(id=ex_id).first()
        if val is None:
            val = ERROR_DB_MSG
        cache.set(key, val, timeout=TIMEOUT)
    return val


def get_user(primary_email):
    user = models.User.query.filter_by(primary_email=primary_email).first()
    return user

