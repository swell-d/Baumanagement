import os

from django.db import models
from django.utils.translation import gettext_lazy as _


class File(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    file = models.FileField(blank=False, upload_to="%Y/%m/%d", verbose_name=_('Files'))

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def delete(self, *args, **kwargs):
        try:
            os.remove(self.file.path)
        except FileNotFoundError:
            pass
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
