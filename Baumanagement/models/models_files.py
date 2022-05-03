import os

from author.decorators import with_author
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel, FileModel


@with_author
class File(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    file = models.FileField(blank=False, upload_to="%Y/%m/%d", verbose_name=_('Files'))

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def delete(self, *args, **kwargs):
        os.remove(self.file.path) if os.path.exists(self.file.path) else None
        for cls in FileModel.__subclasses__():
            for obj in cls.objects.all():
                if self.id in obj.file_ids:
                    obj.file_ids.remove(self.id)
                    obj.save()
        super().delete(*args, **kwargs)
