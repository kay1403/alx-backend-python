#!/usr/bin/env python3
"""GithubOrgClient module"""

import requests
from utils import get_json


class GithubOrgClient:
    """GitHub Organization Client"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org):
        self.org_name = org

    @property
    def org(self):
        """Get organization data"""
        return get_json(self.ORG_URL.format(org=self.org_name))

    @property
    def _public_repos_url(self):
        """Get public repos URL"""
        return self.org["repos_url"]

    def public_repos(self, license=None):
        """Get list of public repos"""
        repos = get_json(self._public_repos_url)
        repo_names = [
            repo["name"] for repo in repos
            if license is None or repo.get("license", {}).get("key") == license
        ]
        return repo_names
