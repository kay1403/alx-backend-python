#!/usr/bin/env python3
"""GithubOrgClient module"""
import requests
from typing import Dict, List
from utils import memoize


class GithubOrgClient:
    """GithubOrgClient class"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name):
        """Constructor"""
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Fetch and memoize the organization information from GitHub."""
        return requests.get(self.ORG_URL.format(org=self._org_name)).json()

    @property
    def _public_repos_url(self) -> str:
        """Get public repositories URL from org"""
        return self.org["repos_url"]

    def public_repos(self, license=None) -> List[str]:
        """List public repos optionally filtered by license"""
        repos = requests.get(self._public_repos_url).json()
        repo_names = [
            repo["name"] for repo in repos
            if not license or self.has_license(repo, license)
        ]
        return repo_names

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repo has a specific license"""
        return repo.get("license", {}).get("key") == license_key
