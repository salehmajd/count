import time

import redis

from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hot_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
@app.route('/')
def hello():
    count = get_hot_count()
    return "Hellow World! This page has been seen {} times. \n".format(count)
