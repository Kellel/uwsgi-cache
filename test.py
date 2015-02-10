import unittest
import random
from cache.cache import CacheManager, Cacher

class CacheManagerTest(unittest.TestCase):
    def setUp(self):
        self.cache = CacheManager('test', 5)
        self.cache.set("data", "data")
        self.cache.set("data2", "data2")

    def test_get(self):
        data = self.cache.get("data")
        self.assertTrue(data == "data")

    def test_set(self):
        self.cache.set("set-test", "test-set")
        self.assertTrue(self.cache.get("set-test") == "test-set")

    def test_keys(self):
        keys = self.cache.keys()
        self.assertTrue(keys == ["data", "data2"])

    def test_exists(self):
        data = self.cache.exists("data")
        self.assertTrue(data == True)

    def test_clear(self):
        self.cache.clear()
        exists = self.cache.exists("data")
        self.assertTrue(exists == False)

        keys = self.cache.keys()
        self.assertTrue(keys == [])

    def test_delete(self):
        self.cache.delete("data")
        data = self.cache.get("data")
        self.assertTrue(data == None)

    def test_delete_doesnt_remove_others(self):
        self.cache.delete("data")
        data = self.cache.get("data2")
        self.assertTrue(data == "data2")

    def test_not_is_fake(self):
        self.assertFalse(self.cache.is_fake())

    def test_case_sensitive(self):
        data = self.cache.get("DATA")
        self.assertTrue(data == None)
        self.cache.set("TEST", "TEST123")
        self.assertTrue(self.cache.get("test") == None)


class MultipleCacheManagerTest(unittest.TestCase):
    def setUp(self):
        self.cache1 = CacheManager('test1', 5)
        self.cache2 = CacheManager('test2', 20)

        self.cache1.set("TEST", "TEST1")
        self.cache2.set("TEST", "TEST2")

    def test_seperate_caches(self):

        data1 = self.cache1.get("TEST")
        data2 = self.cache2.get("TEST")

        self.assertFalse(data1 == data2)

    def test_seperate_clear(self):
        self.cache1.clear()
        self.assertTrue(self.cache1.keys() == [])
        data2 = self.cache2.get("TEST")

        self.assertTrue(data2 == "TEST2")

    def test_uwsgi_clear(self):
        self.assertTrue(self.cache1.get("TEST") == "TEST1")
        self.assertTrue(self.cache2.get("TEST") == "TEST2")

        self.cache1.clear_uwsgi_cache()

        self.assertTrue(self.cache1.keys() == [])
        self.assertTrue(self.cache2.keys() == [])

test_cache = Cacher("testing", 10)

input_val = 0

@test_cache.cache()
def test_cacher(l):
    global input_val
    result = input_val
    input_val = l
    return result


class CacheWrapperText(unittest.TestCase):
    def test_cacher_funcs(self):
        result = test_cacher(10)

        self.assertTrue(result in [0, 10])

        result2 = test_cacher(10)

        self.assertTrue(result == result2)

    def test_cacher_invalidate(self):
        result = test_cacher(10)
        result2 = test_cacher(10)
        self.assertTrue(result == result2)

        test_cache.invalidate()

        result2 = test_cacher(10)
        self.assertFalse(result == result2)

def main():
    unittest.main(module=__name__)

if __name__ == '__main__':
    main()

