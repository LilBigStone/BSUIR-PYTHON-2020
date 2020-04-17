import functools
import unittest


def cached(function):
    func_dict = {}

    @functools.wraps(function)
    def function_counter(*args, **kwargs):
        key = args + tuple(sorted(kwargs.items()))
        if key not in func_dict:
            func_dict[key] = function(*args, **kwargs)
        return func_dict[key]

    return function_counter


@cached
def multiply(a, b):
    return a*b
