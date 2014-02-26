import models
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

TIMEOUT = 5 * 60
ERROR_DB_MSG = 'Value not found in db'

KEY_PAGE = 'page'
KEY_PAGES = 'pages'
KEY_EXERCISES = 'exs'
KEY_EXERCISE = 'ex'

KEY_PROFILE = 'cached_profile'


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


def is_profile_changed(profile_form):
    #return false if the submitted profile form matches the cache, if there
    #is no change, there is no need to post it to the database
    key = KEY_PROFILE
    old_profile = cache.get(key)
    if old_profile != None:
        if old_profile.show_public != profile_form.show_public.data:
            return True
        if old_profile.full_name != profile_form.full_name.data:
            return True
        if old_profile.public_email != profile_form.public_email.data:
            return True
        if old_profile.homepage != profile_form.homepage.data:
            return True
        if old_profile.company != profile_form.company.data:
            return True
        if old_profile.school != profile_form.school.data:
            return True
        if old_profile.location != profile_form.location.data:
            return True
    return False


def clear_cache():
    cache.set(KEY_PROFILE, None)