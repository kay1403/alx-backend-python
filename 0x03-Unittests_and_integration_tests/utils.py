#!/usr/bin/env python3
"""Utils module"""

from typing import Mapping, Sequence, Any, Dict
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access value in nested map using a sequence of keys"""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Dict:
    """Get JSON response from URL"""
    response = requests.get(url)
    return response.json()


def memoize(method):
    """Memoization decorator"""
    attr_name = f"_memoized_{method.__name__}"

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
