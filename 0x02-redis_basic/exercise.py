#!/usr/bin/env python3
"""
Function that defines a Cache class that can be used to store data in Redis.
"""
import redis
from typing import Union, Callable
from functools import wraps
import uuid
import functools


def count_calls(method: Callable) -> Callable:
    """
    function that takes a single method Callable argument
    and returns a Callable
    """
    key = method.__qualname__

    @functools.wraps(method)
    def wrap(self, *args, **kwargs):
        """
        function to increment count and call original method
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrap


def call_history(method):
    '''
    Function to store the history of inputs and outputs
    for a particular function
    '''
    @wraps(method)
    def wrap(self, *args, **kwargs):
        '''
        return results
        '''
        inputs = "{}:inputs".format(method.__qualname__)
        outputs = "{}:outputs".format(method.__qualname__)

        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, result)

        return result
    return wrap


def replay(func: Callable) -> None:
    """ Display the history of calls of a particular function """
    func_name = func.__qualname__
    inputs = f"{func_name}:inputs"
    outputs = f"{func_name}:outputs"

    inputs = cache._redis.lrange(inputs, 0, -1)
    outputs = cache._redis.lrange(outputs, 0, -1)

    count = len(inputs)
    print(f"{func_name} was called {count} times:")

    for inp, out in zip(inputs, outputs):
        inp_str = inp.decode('utf-8')
        out_str = out.decode('utf-8')
        print(f"{func_name}(*{inp_str}) -> {out_str}")


class Cache:
    """
    Class Redis cache.
    """

    def __init__(self):
        """
        Initializes a new instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key, stores the input(redis data) using the key
        and return it.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes,
                                                          int, float, None]:
        """
        Get data and convert it using fn to format you want
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        data from Redis is converted back to a string
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        data from Redis is converted back to an integer
        """
        return self.get(key, fn=int)


if __name__ == '__main__':
    cache = Cache()
