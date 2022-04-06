from django.db import models
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.abstract import BaseModel, AddressModel, FileModel


class CompanyRole(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Role'))

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @property
    def count_companies(self):
        return self.companies.count()

    url = 'companyroles'
    table_fields = 'name',
    search_fields = 'name',
    form_fields = 'name',


class Company(BaseModel, AddressModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Company name'))
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

    url = 'companies'
    table_fields = 'name', 'address', 'email', 'phone', 'role', 'ceo', 'vat_number', 'files'
    search_fields = 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number'
    form_fields = 'open', 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number', 'role'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.accounts.count() == 0:
            eur = Currency.objects.get(id=1)
            Account.objects.create(name=_('Main account'), company=self, currency=eur, created_by=self.created_by)


class Currency(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    code = models.CharField(max_length=3, null=False, blank=False, verbose_name=_('Code'))
    symbol = models.CharField(max_length=3, null=False, blank=False, verbose_name=_('Symbol'), default='')
    rate = models.FloatField(verbose_name=_('Rate'), default=1)

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    url = 'currencies'
    table_fields = 'name', 'code', 'symbol', 'rate'
    search_fields = 'name', 'code', 'symbol', 'rate'
    form_fields = 'open', 'name', 'code', 'symbol', 'rate'


class Account(BaseModel, FileModel):
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='accounts')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Account name'))
    currency = models.ForeignKey(Currency, null=False, blank=False, verbose_name=_('Currency'),
                                 on_delete=models.RESTRICT, related_name='accounts')
    IBAN = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('IBAN'))
    BIC = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('BIC'))

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    def __str__(self):
        return f'{self.company}: {self.name} ({self.currency.code})'

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    url = 'accounts'
    table_fields = 'created', 'company', 'name', 'currency', 'IBAN', 'BIC', 'files'
    search_fields = 'company__name', 'name', 'currency__name', 'IBAN', 'BIC'
    form_fields = 'open', 'company', 'name', 'currency', 'IBAN', 'BIC'


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

    url = 'contacts'
    table_fields = 'created', 'company', 'name', 'email', 'phone', 'position', 'files'
    search_fields = 'company__name', 'name', 'email', 'phone', 'position'
    form_fields = 'open', 'company', 'name', 'email', 'phone', 'position'
