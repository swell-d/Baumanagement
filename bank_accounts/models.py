import re

from author.decorators import with_author
from django.db import models
from django.db.models import Sum, Case, When, F, DecimalField
from django.utils.translation import gettext_lazy as _
from schwifty import IBAN
from schwifty.exceptions import SchwiftyException

from Baumanagement.models.models_company import Company
from Baumanagement.models.models_currency import Currency
from main.models import BaseModel, FileModel


@with_author
class Account(BaseModel, FileModel):
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='accounts')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Account name'))
    currency = models.ForeignKey(Currency, null=False, blank=False, verbose_name=_('Currency'),
                                 on_delete=models.RESTRICT, related_name='accounts', default=Currency.get_EUR_id)
    IBAN = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('IBAN'))
    BIC = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('BIC'))
    bank = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Bank'))

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    def save(self, *args, **kwargs):
        if self.IBAN:
            try:
                iban = IBAN(self.IBAN)
                self.IBAN = iban.compact
                self.BIC = iban.bic.compact
                self.bank = iban.bic.bank_names[0]
            except (SchwiftyException, AttributeError):
                self.IBAN = re.sub(r'\s+', '', str(self.IBAN))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.company}: {self.name} ({self.currency.code})'

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(
            sum1=Sum(Case(When(payments_from__open=True, then=F('payments_from__amount_brutto_positiv'))),
                     output_field=DecimalField(), default=0),
            sum2=Sum(Case(When(payments_to__open=True, then=F('payments_to__amount_brutto_positiv'))),
                     output_field=DecimalField(), default=0))

    urls = 'accounts'
    url_id = 'account_id'
    table_fields = 'company', 'name', 'currency', 'IBAN', 'BIC', 'files', 'balance'
    search_fields = 'company__name', 'name', 'currency__name', 'IBAN', 'BIC'
    form_fields = 'open', 'company', 'name', 'currency', 'IBAN'
