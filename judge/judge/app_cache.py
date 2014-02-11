import models
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

TIMEOUT = 5 * 60
ERROR_DB_MSG = 'Value not found in db'

KEY_PAGE = 'page'
KEY_PAGES = 'pages'
KEY_EXERCISES = 'exs'
KEY_EXERCISE = 'ex'


def reset_exercise_list():
    key = KEY_EXERCISES
    val = models.Exercises.query.all()
    cache.set(key, val, timeout=TIMEOUT)


def reset_exercise(ex_id):
    key = '%s%s' % (KEY_EXERCISE, ex_id)
    val = models.Exercises.query.filter_by(id=ex_id).first()
    cache.set(key, val, timeout=TIMEOUT)


def reset_page_list():
    key = KEY_PAGES
    val = models.PageContent.query.all()
    cache.set(key, val, timeout=TIMEOUT)


def reset_page(pg_id):
    key = '%s%s' % (KEY_PAGE, pg_id)
    val = models.PageContent.query.filter_by(id=pg_id).first()
    cache.set(key, val, timeout=TIMEOUT)
    key = '%s%s' % (KEY_PAGE, val.page)
    cache.set(key, val.content, timeout=TIMEOUT)