from author.decorators import with_author
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from bank_accounts.models import Account
from contracts.models import Contract
from main.models import BaseModel, PriceModel, FileModel


@with_author
class Payment(BaseModel, PriceModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Payment name'))
    date = models.DateField(null=True, blank=True, verbose_name=_('Date'))
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name=_('Contract'),
                                 on_delete=models.RESTRICT, related_name='payments')
    account_from = models.ForeignKey(Account, null=False, blank=False, verbose_name=_('Write-off account'),
                                     on_delete=models.RESTRICT, related_name='payments_from')
    account_to = models.ForeignKey(Account, null=False, blank=False, verbose_name=_('Top-up account'),
                                   on_delete=models.RESTRICT, related_name='payments_to')

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    @property
    def type(self):
        return self.contract.type

    @property
    def currency(self):
        return self.contract.currency

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(project=F('contract__project__name'), company=F('contract__company__name'))

    urls = 'payments'
    url_id = 'payment_id'
    table_fields = 'created', 'project', 'company', 'contract', 'name', 'date', 'files', 'amount_netto', 'vat', 'amount_brutto'
    search_fields = 'project', 'company', 'contract__name', 'name', 'amount_netto', 'vat', 'amount_brutto'
    form_fields = 'open', 'contract', 'name', 'date', 'account_from', 'account_to', 'amount_netto_positiv', 'vat'
