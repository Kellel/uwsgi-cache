uwsgi --http-socket :8000 --eval "import test; test.main()" --cache2 name=test,items=100
