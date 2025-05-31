#!/usr/bin/env python3
"""
Test module for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test org method returns correct value"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected URL"""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://fake.url/repos"}
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, "http://fake.url/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repos"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fake.url/repos"
            client = GithubOrgClient("testorg")
            self.assertEqual(client.public_repos(),
                             ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fake.url/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct bool"""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for public_repos method"""

    @classmethod
    def setUpClass(cls):
        """Mock requests.get and prepare fixtures"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        # Side effects for requests.get().json()
        mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: public_repos returns expected list"""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test: filter repos by license"""
        client = GithubOrgClient("testorg")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
