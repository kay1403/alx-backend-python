#!/usr/bin/env python3
""" Fixture module for client unit tests """

TEST_PAYLOAD = {
    "org": {
        "login": "google",
        "id": 1342004,
        "repos_url": "https://api.github.com/orgs/google/repos"
    },
    "repos": [
        {
            "id": 7697149,
            "name": "dagger",
            "license": {
                "key": "apache-2.0",
                "name": "Apache License 2.0",
                "spdx_id": "Apache-2.0"
            }
        },
        {
            "id": 7776515,
            "name": "flatbuffers",
            "license": {
                "key": "apache-2.0",
                "name": "Apache License 2.0",
                "spdx_id": "Apache-2.0"
            }
        },
        {
            "id": 7787085,
            "name": "volley",
            "license": {
                "key": "other",
                "name": "Other",
                "spdx_id": "OTHER"
            }
        }
    ]
}
