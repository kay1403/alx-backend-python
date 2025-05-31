#!/usr/bin/env python3
"""Client module for GithubOrgClient"""

from typing import List, Dict
from utils import get_json
from functools import cached_property


class GithubOrgClient:
    """GithubOrgClient class"""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        """Initialize with org name"""
        self._org_name = org_name

    @cached_property
    def org(self) -> Dict:
        """Return organization info"""
        return get_json(self.ORG_URL.format(self._org_name))

    @cached_property
    def _public_repos_url(self) -> str:
        """Return repos URL"""
        return self.org["repos_url"]

    def public_repos(self, license: str = None) -> List[str]:
        """Return public repos, optionally filtered by license"""
        repos = get_json(self._public_repos_url)
        repo_names = []

        for repo in repos:
            if license is None or self.has_license(repo, license):
                repo_names.append(repo["name"])
        return repo_names

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repo has a specific license"""
        license_info = repo.get("license")
        return license_info is not None and license_info.get("key") == license_key
