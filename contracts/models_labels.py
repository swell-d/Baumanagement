from author.decorators import with_author
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel, Label


@with_author
class ContractLabel(Label, BaseModel):
    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')

    @property
    def count(self):
        return self.contracts.count()

    urls = 'contractlabels'
    url_id = 'contractlabel_id'
    table_fields = 'path', 'name'
    search_fields = 'path',
    form_fields = 'name', 'parent', 'color'
