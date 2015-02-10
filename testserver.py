from cache import CacheManager, Cacher
from bottle import route, Bottle

app = Bottle()
caches = {
        'test': CacheManager('test', 100),
        '2': CacheManager('2', 2)
    }
cache = CacheManager('test', 100)

@app.route('/')
def index():
    cache.set('test', '100')
    return cache.get('test')

@app.get('/clear/<cache>/')
def clear(cache):
    if cache in caches:
        caches[cache].clear()

@app.get('/keys/<cache>/')
def keys(cache):
    if cache in caches:
        return caches[cache].keys()

@app.get('/<cache>/<key>/')
def get_key(cache, key):
    if cache in caches:
        return caches[cache].get(key)

@app.get('/<cache>/<key>/<value>/')
def set_key(cache, key, value):
    if cache in caches:
        caches[cache].set(key, value)

x = 1

@app.get('/1/<data>')
def cache_data(data):
    result = data + x
    global x
    x = x + 1
    return result



application = app
