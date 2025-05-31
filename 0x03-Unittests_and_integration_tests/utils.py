#!/usr/bin/env python3
""" Utility functions for testing """

def access_nested_map(nested_map, path):
    """Access a nested map with a list of keys"""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url):
    """Mocked function for getting JSON from a URL"""
    import requests
    response = requests.get(url)
    return response.json()


def memoize(method):
    """Memoize decorator"""
    attr_name = "_{}".format(method.__name__)

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)
    return wrapper
