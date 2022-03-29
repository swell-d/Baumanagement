import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.abstract import BaseModel
from Baumanagement.models.models import Company, Project, Contract, Bill, Payment


class File(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    file = models.FileField(blank=True, upload_to="%Y/%m/%d", verbose_name=_('Files'))

    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.RESTRICT, related_name='files')
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.RESTRICT, related_name='files')
    contract = models.ForeignKey(Contract, null=True, blank=True, on_delete=models.RESTRICT, related_name='files')
    bill = models.ForeignKey(Bill, null=True, blank=True, on_delete=models.RESTRICT, related_name='files')
    payment = models.ForeignKey(Payment, null=True, blank=True, on_delete=models.RESTRICT, related_name='files')

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def delete(self, *args, **kwargs):
        try:
            os.remove(self.file.path)
        except FileNotFoundError:
            pass
        super().delete(*args, **kwargs)


FilesClasses = {'File': File}
