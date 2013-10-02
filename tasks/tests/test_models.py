import sure
from django.test import TestCase
from ..models import Task
from . import factories


class TaskModelCase(TestCase):
    """Task model case"""

    def test_generate_keys(self):
        """Test generate keys"""
        task = Task()
        task.generate_keys()
        task.private_key.should.not_be.none
        task.public_key.should.not_be.none

    def test_generate_keys_on_save(self):
        """Test generate keys on save"""
        task = factories.TaskFactory()
        task.save()
        task.private_key.should.not_be.none
        task.public_key.should.not_be.none
