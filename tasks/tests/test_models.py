import sure
from unittest.mock import MagicMock
from django.test import TestCase
from ..exceptions import NotAllowedWithThisStatus, ConnectionFailed
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
        task.private_key.should.not_be.equal('')
        task.public_key.should.not_be.equal('')

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
        self._mock_logger()

    def _mock_paramiko(self):
        """Mock paramiko ssh client"""
        self._orig_ssh_client = models.paramiko.SSHClient
        models.paramiko.SSHClient = MagicMock()

    def _mock_logger(self):
        """Mock logger"""
        self._orig_logger = models.logger
        models.logger = MagicMock()

    def tearDown(self):
        models.paramiko.SSHClient = self._orig_ssh_client
        models.logger = self._orig_logger

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

    def test_raise_when_connection_failed(self):
        """Test raise exception when connection failed"""
        job = factories.JobFactory(status=models.Job.STATUS_IN_PROGRESS)
        models.paramiko.SSHClient.return_value.connect.side_effect =\
            Exception()
        (lambda: job.connection).should.throw(ConnectionFailed)

    def test_preform_fail_when_not_new(self):
        """Test perform fail when not new"""
        job = factories.JobFactory(status=models.Job.STATUS_IN_PROGRESS)
        job.perform.should.called_with().throw(
            NotAllowedWithThisStatus,
        )

    def _create_channel(self, result: str) -> MagicMock:
        """Create paramiko channel"""
        return MagicMock(read=MagicMock(return_value=result))

    def test_preform_success(self):
        """Test perform success"""
        job = factories.JobFactory(status=models.Job.STATUS_NEW)
        job._connection = MagicMock()
        job._connection.exec_command.return_value =\
            [self._create_channel(val) for val in ['input', 'output', 'error']]
        job.perform()
        job.output.should.be.equal('output')
        job.status.should.be.equal(models.Job.STATUS_SUCCESS)

    def test_perform_connection_failed(self):
        """Test perform and connection failed"""
        job = factories.JobFactory(status=models.Job.STATUS_NEW)
        job._connection = MagicMock()
        job._connection.exec_command.side_effect = ConnectionFailed
        job.perform()
        models.logger.log.call_count.should.be.equal(1)
        job.status.should.be.equal(models.Job.STATUS_FAILED)

    def test_perform_exception(self):
        """Test perform exception"""
        job = factories.JobFactory(status=models.Job.STATUS_NEW)
        job._connection = MagicMock()
        job._connection.exec_command.side_effect = Exception
        job.perform()
        models.logger.exception.call_count.should.be.equal(1)
        job.status.should.be.equal(models.Job.STATUS_FAILED)
