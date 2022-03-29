from django.db import models
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.abstract import BaseModel, FileModel
from Baumanagement.models.models import Company, Project, Contract, Bill, Payment


class File(BaseModel, FileModel):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.RESTRICT, related_name='files')
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.RESTRICT, related_name='files')
    contract = models.ForeignKey(Contract, null=True, blank=True, on_delete=models.RESTRICT, related_name='files')
    bill = models.ForeignKey(Bill, null=True, blank=True, on_delete=models.RESTRICT, related_name='files')
    payment = models.ForeignKey(Payment, null=True, blank=True, on_delete=models.RESTRICT, related_name='files')

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')


FilesClasses = {'File': File}
