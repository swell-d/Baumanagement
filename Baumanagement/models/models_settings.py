from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_projects import Project


class Settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    active_project = models.ForeignKey(Project, on_delete=models.RESTRICT,
                                       null=True, blank=True, related_name='settings')
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    sort = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _('Settings')

    def __str__(self):
        return self.user.username
