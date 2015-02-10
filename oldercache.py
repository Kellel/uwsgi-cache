import uwsgi

class Cache(object):
    def __init__(self, name, expire):
        self.name = name
        self.expire = expire


    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            key = "|".join(map(str, [fn.func_name, args, kwargs]))
            if uwsgi.cache_exists(key, self.name):
                print("[CACHE] Hit")
                return uwsgi.cache_get(key, self.name)
            else:
                print("[CACHE] Miss")
                res = str(fn(*args, **kwargs))
                uwsgi.cache_set(key, res, self.expire, self.name)
                return res
        return wrapper

    def invalidate(self, fn):
        def wrapper(*args, **kwargs):
            uwsgi.cache_clear(self.name)
            return fn(*args, **kwargs)
        return wrapper

class CacheInvalidate(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, fn):
        def wrapper (*args, **kwargs):
            uwsgi.cache_clear(self.name)
            return fn(*args, **kwargs)
        return wrapper

## Use the Following for testing
##

import bottle

application = bottle.Bottle()

@application.route('/test')
@Cache("index", 1)
def index():
    return {"1111": "0000"}

@application.route('/invalid')
@CacheInvalidate("index")
def invalid():
    return "Herp"

