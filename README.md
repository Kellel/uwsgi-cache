Uwsgi Caching package
=====================

This is a wrapper for the low level uwsgi cache module. It gives the ability to have named sub-cache groups that can be individualy cleared.

Running uWSGI
-------------

To enable the cache subsystem within uWSGI use the following command line arguments

    --cache2 name=api,items=1000

Tests
-----

Because this module uses uwsgi for the cache backend you must have uwsgi installed to run it.

    mkvirtualenv uwsgi-cache
    ./run.sh

