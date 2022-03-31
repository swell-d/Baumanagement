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

    table_fields = 'name', 'address', 'email', 'phone', 'role', 'ceo', 'vat_number', 'files'
    search_fields = 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number'
    form_fields = 'open', 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number', 'role'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.accounts.count() == 0:
            Account.objects.create(name=_('Main account'), company=self)


class Account(BaseModel, FileModel):
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Account name'))
    IBAN = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('IBAN'))
    BIC = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('BIC'))

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    table_fields = 'created', 'company', 'name', 'IBAN', 'BIC', 'files'
    search_fields = 'company__name', 'name', 'IBAN', 'BIC'
    form_fields = 'open', 'company', 'name', 'IBAN', 'BIC'
