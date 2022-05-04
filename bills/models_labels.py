from author.decorators import with_author
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel, Label


@with_author
class BillLabel(Label, BaseModel):
    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')

    @property
    def count(self):
        return self.bills.count()

    urls = 'billlabels'
    url_id = 'billlabel_id'
    table_fields = 'path', 'name'
    search_fields = 'path',
    form_fields = 'name', 'parent', 'color'
