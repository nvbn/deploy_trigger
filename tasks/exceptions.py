class NotAllowedWithThisStatus(Exception):
    """Not allowed with this status"""

    def __init__(self, job: 'tasks.models.Job'):
        super(NotAllowedWithThisStatus, self).__init__(
            'Action for job {} not allowed with status={}'.format(
                job, job.status,
            )
        )
