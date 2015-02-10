from uwsgi_cache.cache import CacheManager, Cacher

import random

test_cache = Cacher("Testing", 10)

# simple function to return a number
@test_cache.cache()
def get_num(x):
    return x + random.randint(0, 100)

# The cache should cause all the numbers to be the same
for _ in range(10):
    print(get_num(10))
