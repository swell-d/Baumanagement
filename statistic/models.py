from django.db import models

from django.utils.translation import gettext_lazy as _


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
