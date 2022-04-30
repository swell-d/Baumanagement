import re

from author.decorators import with_author
from django.db import models
from django.db.models import F, Sum, Case, When, DecimalField
from django.utils.translation import gettext_lazy as _
from schwifty import IBAN
from schwifty.exceptions import SchwiftyException

from Baumanagement.models.abstract import BaseModel, AddressModel, FileModel
from Baumanagement.models.models_currency import Currency


@with_author
class CompanyRole(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Role'), unique=True)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @property
    def count(self):
        return self.companies.count()

    urls = 'companyroles'
    url_id = 'companyrole_id'
    table_fields = 'name',
    search_fields = 'name',
    form_fields = 'name',


@with_author
class Company(BaseModel, AddressModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Company name'), unique=True)
    email = models.EmailField(null=False, blank=True, verbose_name=_('E-mail'))
    phone = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Phone'))
    role = models.ManyToManyField(CompanyRole, blank=False, verbose_name=_('Role'), related_name='companies')
    ceo = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('CEO'))
    vat_number = models.CharField(max_length=16, null=False, blank=True, verbose_name=_('VAT number'))

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    urls = 'companies'
    url_id = 'company_id'
    table_fields = 'id', 'name', 'address', 'email', 'phone', 'role', 'ceo', 'vat_number', 'files'
    search_fields = 'id', 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number'
    form_fields = 'open', 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number', 'role'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.accounts.count() == 0:
            eur = Currency.objects.get(id=1)
            Account.objects.create(name=_('Main account'), company=self, currency=eur)


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
            except SchwiftyException:
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


@with_author
class Contact(BaseModel, FileModel):
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='contacts')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    email = models.EmailField(null=False, blank=True, verbose_name=_('E-mail'))
    phone = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Phone'))
    position = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Position'))

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    urls = 'contacts'
    url_id = 'contact_id'
    table_fields = 'company', 'name', 'email', 'phone', 'position', 'files'
    search_fields = 'company__name', 'name', 'email', 'phone', 'position'
    form_fields = 'open', 'company', 'name', 'email', 'phone', 'position'
