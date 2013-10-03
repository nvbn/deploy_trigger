from unittest.mock import MagicMock
import sure
from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import User


class RepositoryViewCase(TestCase):
    """Repository view case"""

    def setUp(self):
        self.api_client = APIClient()
        self._mock_github()
        self._create_user()
        self.url = '/api/v1/repositories/'

    def _create_user(self):
        """Create user and authenticate"""
        self.user = User.objects.create_user('test', 'test@test.test', 'test')
        self.api_client.login(
            username='test',
            password='test',
        )

    def _mock_github(self):
        """Mock github client"""
        self._orig_github = User.github
        User.github = MagicMock()

    def tearDown(self):
        User.github = self._orig_github

    def test_list_repositories(self):
        """Test list repositories"""
        User.github.get_user.return_value.get_repos.return_value =\
            [MagicMock()] * 10
        response = self.api_client.get(self.url)
        len(response.data).should.be.equal(10)
