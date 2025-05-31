#!/usr/bin/env python3
"""
Unit tests and integration tests for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @patch("client.get_json")
    @patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """Test public_repos returns correct data"""
        mock_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"
        mock_get_json.return_value = TEST_PAYLOAD[1]["repos_payload"]  # repos_payload fixture

        client = GithubOrgClient("test-org")
        result = client.public_repos()

        expected = TEST_PAYLOAD[2]["expected_repos"]
        self.assertEqual(result, expected)
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")

    @patch("client.get_json")
    @patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock)
    def test_public_repos_with_license(self, mock_repos_url, mock_get_json):
        """Test public_repos returns only repos with a given license"""
        mock_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"
        mock_get_json.return_value = TEST_PAYLOAD[1]["repos_payload"]

        client = GithubOrgClient("test-org")
        result = client.public_repos(license="apache-2.0")

        expected = TEST_PAYLOAD[3]["apache2_repos"]
        self.assertEqual(result, expected)
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")
