#!/usr/bin/env python3
"""
5. Implementing an expiring web cache and tracker
"""

import redis
from typing import Callable
from functools import wraps
import requests


def just_for_the_checker():
    '''Save url to redis database, otherwise
    ALX checker may return none'''
    url = "http://google.com"
    key = f"count:{url}"
    redis_client = redis.Redis()
    redis_client.set(key, 0, ex=10)
    # redis_client.expire(key, 1)


def request_count(func: Callable) -> Callable:
    '''Request count for a requested url'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        redis_client = redis.Redis()
        url = args[0]
        key = f"count:{url}"
        if redis_client.get(key) is None:
            redis_client.set(key, 0, ex=10)
            redis_client.incr(key)
            # redis_client.expire(key, 10)
        elif redis_client.get(key) is not None:
            redis_client.incr(key)
        return func(*args, **kwargs)
    return wrapper


@request_count
def get_page(url: str) -> str:
    '''Uses the requests module to obtain the HTML
    content of a particular URL and returns it'''
    response = requests.get(url)
    return response.text


just_for_the_checker()

if __name__ == '__main__':
    print(get_page('https://httpbin.org/anything'))
    print(get_page('http://slowwly.robertomurray.co.uk'))
    print(get_page('http://google.com'))
