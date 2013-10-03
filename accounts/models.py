from github import Github
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model"""

    @property
    def github(self) -> Github:
        """Get github api instance for user"""
        if not hasattr(self, '_github'):
            self._github = Github(self.social_auth.get().tokens)
        return self._github
