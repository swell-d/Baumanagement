from author.decorators import with_author
from django.db import models
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_currency import Currency
from main.models import BaseModel, AddressModel, FileModel


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
            from bank_accounts.models import Account
            eur = Currency.objects.get(id=1)
            Account.objects.create(name=_('Main account'), company=self, currency=eur)
