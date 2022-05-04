from author.decorators import with_author
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel


@with_author
class ContractLabel(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    parent = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True,
                               verbose_name=_('Classify label under'), related_name='children')

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')

    def __str__(self):
        return f'{self.parent}/{self.name}' if self.parent else self.name

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @property
    def count(self):
        return self.contracts.count()

    urls = 'contractlabels'
    url_id = 'contractlabel_id'
    table_fields = 'name',
    search_fields = 'name',
    form_fields = 'name', 'parent'
