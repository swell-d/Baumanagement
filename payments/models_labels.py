from author.decorators import with_author
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel, Label


@with_author
class PaymentLabel(Label, BaseModel):
    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')

    @property
    def count(self):
        return self.payments.count()

    urls = 'paymentlabels'
    url_id = 'paymentlabel_id'
    table_fields = 'path', 'name'
    search_fields = 'path',
    form_fields = 'name', 'parent', 'color'
