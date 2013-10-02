import sure
from unittest.mock import MagicMock
from django.test import TestCase
from .. import jobs
from ..models import Job
from . import factories


class PerformJobCase(TestCase):
    """Perform job case"""

    def setUp(self):
        self._mock_perform()
        self._mock_logger()

    def _mock_perform(self):
        """Mock Job.perform method"""
        self._orig_perform = Job.perform
        Job.perform = MagicMock()

    def _mock_logger(self):
        """Mock logger"""
        self._orig_logger = jobs.logger
        jobs.logger = MagicMock()

    def tearDown(self):
        Job.perform = self._orig_perform
        jobs.logger = self._orig_logger

    def test_perform(self):
        """Test perform"""
        job = factories.JobFactory()
        jobs.perform_job(job.id)
        Job.perform.call_count.should.be.equal(1)

    def test_job_doesnt_exists(self):
        """Test job doesnt exists"""
        jobs.perform_job(-1)
        Job.perform.call_count.should.be.equal(0)
        jobs.logger.exception.call_count.should.be.equal(1)
