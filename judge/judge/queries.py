import models
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

TIMEOUT = 5 * 60
KEY_PAGE = 'page-'
ERROR_DB_MSG = 'Value not found in db'


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
