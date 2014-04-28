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
    print "Getting profile for user: ", primary_email
    #key = KEY_PROFILE
    #val = cache.get(key)
    # if val is None:
    #     user = models.User.query.filter_by(primary_email=primary_email).first()
    #     val =  models.Profile.query.get(user.user_id)
    #     if val is None:
    #         val = ERROR_DB_MSG
    #     else:
    #         cache.set(key, val, timeout=TIMEOUT)
    if primary_email:
        user = models.User.query.filter_by(primary_email=primary_email).first()
        val =  models.Profile.query.get(user.user_id)
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


def get_profile_from_id(profile_id):
    #gets a users profile for viewing by the profile id found from querying
    profile = models.Profile.query.get(profile_id)
    return profile


def get_exercise_statistic(profile_id, exercise_id):
    statistic = models.Statistics.query.filter_by(profile_id=profile_id, exercise_id=exercise_id).first()
    return statistic


def get_users_statistics(primary_email, profile_id):
    #returns a list of a users exercise statistics
    if profile_id == None:
        profile_id = get_profile(primary_email).profile_id
    statistics = models.Statistics.query.filter_by(profile_id=profile_id).all()
    list = []
    #builds a list of data for each exercise to pass to the template
    for s in statistics:
        stats = {}
        stats['exercise_id'] = s.exercise_id
        if s.memory != None:
            stats['memory'] = s.memory
        else:
            stats['memory'] = "Incomplete"
        if s.time != None:
            stats['time'] = s.time
        else:
            stats['time'] = "Incomplete"
        stats['attempts'] = s.attempts
        if s.passed == True:
            stats['passed'] = "Passed"
        else:
            stats['passed'] = "Failed"
        list.append(stats)
    return list