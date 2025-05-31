#!/usr/bin/env python3
""" GithubOrgClient module """

import requests
from typing import List, Dict
from utils import memoize


class GithubOrgClient:
    """A client for GitHub organization data"""
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str):
        """Initialize with organization name"""
        self.org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Fetch organization information from GitHub"""
        url = self.ORG_URL.format(org=self.org_name)
        return requests.get(url).json()

    @property
    def _public_repos_url(self) -> str:
        """Get the URL for public repos"""
        return self.org.get("repos_url")

    @memoize
    def repos_payload(self) -> List[Dict]:
        """Get the list of repos from the public repos URL"""
        return requests.get(self._public_repos_url).json()

    def public_repos(self, license: str = None) -> List[str]:
        """Get public repository names filtered by license if provided"""
        repos = self.repos_payload
        if license is None:
            return [repo["name"] for repo in repos]
        return [
            repo["name"]
            for repo in repos
            if repo.get("license") and repo["license"].get("key") == license
        ]
