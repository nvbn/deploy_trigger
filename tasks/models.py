from io import BytesIO
import paramiko
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from .exceptions import NotAllowedWithThisStatus, ConnectionFailed
from . import logger


class Task(models.Model):
    """Task model"""
    repository = models.CharField(
        max_length=300, verbose_name=_('repository'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created'),
    )
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))
    branch = models.CharField(max_length=300, verbose_name=_('branch'))
    branch_match_regex = models.BooleanField(
        default=False, verbose_name=_('branch match regex'),
    )
    name = models.CharField(max_length=300, verbose_name=_('name'))
    server = models.CharField(max_length=300, verbose_name=_('server'))
    public_key = models.TextField(
        editable=False, verbose_name=_('public key'),
    )
    private_key = models.TextField(
        editable=False, verbose_name=_('private key'),
    )
    script = models.TextField(verbose_name=_('script'))

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __unicode__(self):
        return self.name

    def generate_keys(self):
        """Generate public and private key"""
        key = paramiko.RSAKey.generate(2048)
        self.public_key = key.get_base64()
        private_key = BytesIO()
        key.write_private_key(private_key)
        self.private_key = private_key.getvalue().decode()

    def get_connection_args(self) -> dict:
        """Get connection args"""
        args = {}
        user, host = self.server.split('@')
        args['hostname'] = host
        args['username'] = user
        if ':' in host:
            host, port = host.split(':')
            args['hostname'] = host
            args['port'] = int(port)
        return args

    def save(self, *args, **kwargs):
        """Generate key if not present and save"""
        if not (self.private_key or self.public_key):
            self.generate_keys()
        return super(Task, self).save(*args, **kwargs)


class Job(models.Model):
    """Task job"""
    STATUS_NEW = 0
    STATUS_IN_PROGRESS = 1
    STATUS_SUCCESS = 2
    STATUS_FAILED = 3
    STATUSES = (
        (STATUS_NEW, _('new')),
        (STATUS_IN_PROGRESS, _('in progress')),
        (STATUS_SUCCESS, _('success')),
        (STATUS_FAILED, _('failed')),
    )

    TRIGGERED_MANUAL = 0
    TRIGGERED_PUSH = 1
    TRIGGERED_TYPES = (
        (TRIGGERED_MANUAL, _('manual')),
        (TRIGGERED_PUSH, _('push')),
    )

    task = models.ForeignKey(Task, verbose_name=_('status'))
    status = models.PositiveSmallIntegerField(
        default=STATUS_NEW, choices=STATUSES, verbose_name=_('status'),
    )
    input = models.TextField(blank=True, null=True, verbose_name=_('input'))
    output = models.TextField(blank=True, null=True, verbose_name=_('output'))
    started = models.DateTimeField(
        auto_now_add=True, verbose_name=_('started'),
    )
    finished = models.DateTimeField(
        blank=True, null=True, verbose_name=_('finished'),
    )
    triggered = models.PositiveSmallIntegerField(
        choices=TRIGGERED_TYPES, verbose_name=_('triggred'),
    )

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    @property
    def connection(self) -> paramiko.SSHClient:
        """Get ssh connection"""
        if self.status != self.STATUS_IN_PROGRESS:
            raise NotAllowedWithThisStatus(self)

        if not hasattr(self, '_connection'):
            self._connection = paramiko.SSHClient()
            self._connection.set_missing_host_key_policy(
                paramiko.AutoAddPolicy,
            )
            try:
                self._connection.connect(**self.task.get_connection_args())
            except Exception as e:
                raise ConnectionFailed(e)
        return self._connection

    def perform(self):
        """Perform job"""
        if self.status != self.STATUS_NEW:
            raise NotAllowedWithThisStatus(self)
        self.status = self.STATUS_IN_PROGRESS
        self.input = self.task.script
        try:
            stdout = self.connection.exec_command(self.input)[1]
            self.output = stdout.read()
            self.status = self.STATUS_SUCCESS
        except ConnectionFailed:
            self.status = self.STATUS_FAILED
            logger.log('Connection failed', exc_info=True, extra={
                'job': self,
            })
        except Exception as e:
            self.status = self.STATUS_FAILED
            logger.exception('Job failed: {}'.format(e))
        self.save()
