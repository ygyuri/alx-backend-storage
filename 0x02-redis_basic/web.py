#!/usr/bin/env python3
'''
function to implement a get_page function
(prototype: def get_page(url: str) -> str:).
'''
from typing import Callable
import requests
import redis
from functools import wraps

# create Redis client
redis_client = redis.Redis()


def url_count(method: Callable) -> Callable:
    '''
    Function for tracking number of times a function is called
    '''
    @wraps(method)
    def wrapper(*args, **kwargs):
        url = args[0]
        redis_client.incr(f"count:{url}")
        cached = redis_client.get(f'{url}')
        if cached:
            return cached.decode('utf-8')
        redis_client.setex(f'{url}, 10, {method(url)}')
        return method(*args, **kwargs)
    return wrapper


@url_count
def get_page(url: str) -> str:
    """
    get a page content with cache and tracker
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
