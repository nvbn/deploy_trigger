import sure
from mock import MagicMock
from django.test import TestCase
from ..exceptions import NotAllowedWithThisStatus
from .. import models
from . import factories


class TaskModelCase(TestCase):
    """Task model case"""

    def test_generate_keys(self):
        """Test generate keys"""
        task = models.Task()
        task.generate_keys()
        task.private_key.should.not_be.none
        task.public_key.should.not_be.none

    def test_generate_keys_on_save(self):
        """Test generate keys on save"""
        task = factories.TaskFactory()
        task.save()
        task.private_key.should.not_be.none
        task.public_key.should.not_be.none

    def test_get_connection_args(self):
        """Test get connectiona args"""
        task = factories.TaskFactory(server='user@host')
        task.get_connection_args().should.be.equal({
            'username': 'user',
            'hostname': 'host',
        })

    def test_get_connection_args_with_port(self):
        """Test get connection args with port"""
        task = factories.TaskFactory(server='user@host:123')
        task.get_connection_args().should.be.equal({
            'username': 'user',
            'hostname': 'host',
            'port': 123,
        })


class JobModelCase(TestCase):
    """Job model case"""

    def setUp(self):
        self._mock_paramiko()

    def _mock_paramiko(self):
        """Mock paramiko ssh client"""
        self._orig_ssh_client = models.paramiko.SSHClient
        models.paramiko.SSHClient = MagicMock()

    def tearDown(self):
        models.paramiko.SSHClient = self._orig_ssh_client

    def test_create_connection_when_in_progress(self):
        """Test create connection when in progress"""
        job = factories.JobFactory(status=models.Job.STATUS_IN_PROGRESS)
        job.connection.should.not_be.none

    def test_not_create_connection_when_not_in_progress(self):
        """
        Test raise exception when create
        connection if job not in progress
        """
        job = factories.JobFactory(status=models.Job.STATUS_NEW)
        (lambda: job.connection).should.throw(NotAllowedWithThisStatus)
