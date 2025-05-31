#!/usr/bin/env python3
"""Utilities module"""

import requests


def get_json(url):
    """Get JSON from URL"""
    response = requests.get(url)
    return response.json()
