from django_rq import job
from .models import Job
from . import logger


@job
def perform_job(job_id: int):
    """Perform job"""
    try:
        Job.objects.get(id=job_id).perform()
    except Job.DoesNotExist as e:
        logger.exception('Job not found: {}'.format(e))
