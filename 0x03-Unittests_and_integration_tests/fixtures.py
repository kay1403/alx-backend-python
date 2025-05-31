#!/usr/bin/env python3
"""Fixtures for integration tests"""

TEST_PAYLOAD = [
    (
        {"login": "google"},
        [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}}
        ],
        ["repo1", "repo2", "repo3"],
        ["repo1", "repo3"]
    )
]
