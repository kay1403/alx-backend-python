#!/usr/bin/env python3
"""Test client module"""

import unittest
from unittest.mock import patch, PropertyMock

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @patch("client.get_json")
    def test_org(self, mock_get_json):
        """Test org returns correct value"""
        expected = {"login": "google"}
        mock_get_json.return_value = expected
        client = GithubOrgClient("google")
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected value"""
        with patch.object(GithubOrgClient,
                          "org",
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url,
                             "https://api.github.com/orgs/google/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos method"""
        mock_get_json.return_value = TEST_PAYLOAD["repos"]
        with patch.object(GithubOrgClient,
                          "_public_repos_url",
                          new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/google/repos"
            client = GithubOrgClient("google")
            repos = client.public_repos()
            expected = ["dagger", "flatbuffers", "volley"]
            self.assertEqual(repos, expected)
            mock_get_json.assert_called_once()
            mock_repos_url.assert_called_once()

    @patch("client.get_json")
    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos with license filter"""
        mock_get_json.return_value = TEST_PAYLOAD["repos"]
        with patch.object(GithubOrgClient,
                          "_public_repos_url",
                          new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/google/repos"
            client = GithubOrgClient("google")
            repos = client.public_repos(license="apache-2.0")
            expected = ["dagger"]
            self.assertEqual(repos, expected)


if __name__ == "__main__":
    unittest.main()
