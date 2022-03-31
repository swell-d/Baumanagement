from django.db import models
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.abstract import BaseModel, FileModel


class Comment(BaseModel, FileModel):
    name = models.TextField(null=False, blank=False, verbose_name=_('Comment'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    table_fields = 'created', 'name'
    search_fields = 'name',
    form_fields = 'name',