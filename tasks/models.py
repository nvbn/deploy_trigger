from io import BytesIO
import paramiko
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Task(models.Model):
    """Task model"""
    repository = models.CharField(
        max_length=300, verbose_name=_('repository'),
    )
    user = models.ForeignKey(User, verbose_name=_('user'))
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
