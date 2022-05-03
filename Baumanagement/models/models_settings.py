from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_currency import Currency
from Baumanagement.models.models_projects import Project


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    active_project = models.ForeignKey(Project, on_delete=models.RESTRICT,
                                       null=True, blank=True, related_name='settings')
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    sort = models.JSONField(default=dict, null=True, blank=True)
    default_currency = models.ForeignKey(Currency, on_delete=models.RESTRICT, default=Currency.get_EUR_id)
    img = models.ImageField(verbose_name=_('Image'), null=True)
    datetime_format = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Datetime format'),
                                       default="%d.%m.%Y %H:%M")
    date_format = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Date format'),
                                       default="%d.%m.%y")

    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _('Settings')

    def __str__(self):
        return self.user.username


class Visits(models.Model):
    page = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Page'), unique=True)
    count = models.BigIntegerField(verbose_name=_('Visits'), default=0)

    class Meta:
        verbose_name = _('Visits')
        verbose_name_plural = _('Visits')

    def __str__(self):
        return f'{self.page} :: {self.count}'


class SearchQueries(models.Model):
    page = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Page'))
    query = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Query'))
    count = models.BigIntegerField(verbose_name=_('Visits'), default=0)

    class Meta:
        verbose_name = _('Search query')
        verbose_name_plural = _('Search queries')

    def __str__(self):
        return f'{self.page} :: {self.query} :: {self.count}'
