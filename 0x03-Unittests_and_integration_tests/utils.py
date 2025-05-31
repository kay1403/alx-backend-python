#!/usr/bin/env python3
"""Utils module: access_nested_map, get_json, and memoize."""
from typing import Mapping, Any, Sequence
import requests
from functools import wraps


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access value in nested map using a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Any:
    """Get JSON content from a URL."""
    response = requests.get(url)
    return response.json()


def memoize(method):
    """Decorator to cache the result of a method."""
    attr_name = f"_memoized_{method.__name__}"

    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
