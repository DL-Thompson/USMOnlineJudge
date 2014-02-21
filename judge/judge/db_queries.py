import models
from app_cache import cache, TIMEOUT, ERROR_DB_MSG, KEY_PAGE, KEY_PAGES, KEY_EXERCISE, KEY_EXERCISES, KEY_PROFILE


def get_page_content(page_title):
    key = '%s%s' % (KEY_PAGE, page_title)
    val = cache.get(key)
    if val is None:
        print 'cache miss'
        val = models.PageContent.query.filter_by(page=page_title).first().get_content()
        if val is None:
            val = ERROR_DB_MSG
        cache.set(key, val, timeout=TIMEOUT)
    return val


def get_page(pg_id):
    key = '%s%s' % (KEY_PAGE, pg_id)
    val = cache.get(key)
    if val is None:
        print 'cache miss'
        val = models.PageContent.query.filter_by(id=pg_id).first()
        if val is None:
            val = ERROR_DB_MSG
        cache.set(key, val, timeout=TIMEOUT)
    return val


def get_pages():
    key = KEY_PAGES
    val = cache.get(key)
    if val is None:
        print 'cache miss'
        val = models.PageContent.query.all()
        if val is None:
            val = ERROR_DB_MSG
        cache.set(key, val, timeout=TIMEOUT)
    return val


def get_exercise_list():
    key = KEY_EXERCISES
    val = cache.get(key)
    if val is None:
        print 'cache miss'
        val = models.Exercises.query.all()
        if val is None:
            val = ERROR_DB_MSG
        cache.set(key, val, timeout=TIMEOUT)
    return val


def get_exercise(ex_id):
    key = '%s%s' % (KEY_EXERCISE, ex_id)
    val = cache.get(key)
    if val is None:
        print 'cache miss'
        val = models.Exercises.query.filter_by(id=ex_id).first()
        if val is None:
            val = ERROR_DB_MSG
        cache.set(key, val, timeout=TIMEOUT)
    return val


def get_user(primary_email):
    user = models.User.query.filter_by(primary_email=primary_email).first()
    return user


def get_profile(primary_email):
    #retrieves and stores the user profile in the cache so the database
    #doesn't need to be queried
    key = KEY_PROFILE
    val = cache.get(key)
    if val is None:
        user = models.User.query.filter_by(primary_email=primary_email).first()
        val =  models.Profile.query.get(user.user_id)
        if val is None:
            val = ERROR_DB_MSG
        cache.set(key, val, timeout=TIMEOUT)
    return val


def get_public_profile(primary_email):
    #searches for a users public profile and returns it if one exists
    user = get_user(primary_email)
    if not user:
        return None
    profile = models.Profile.query.get(user.user_id)
    if profile != None and profile.show_public == True:
        return profile
    else:
        return None
