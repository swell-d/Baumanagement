from author.decorators import with_author
from django.db import models
from django.utils.translation import gettext_lazy as _

from companies.models_labels import CompanyLabel
from currencies.models import Currency
from main.models import BaseModel, AddressModel, FileModel


@with_author
class Company(BaseModel, AddressModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Company name'), unique=True)
    email = models.EmailField(null=False, blank=True, verbose_name=_('E-mail'))
    phone = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Phone'))
    label = models.ManyToManyField(CompanyLabel, blank=True, verbose_name=_('Labels'), related_name='companies')
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
    table_fields = 'id', 'name', 'address', 'email', 'phone', 'label', 'ceo', 'vat_number', 'files'
    search_fields = 'id', 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number'
    form_fields = 'open', 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number', 'label'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.accounts.count() == 0:
            from bank_accounts.models import Account
            eur = Currency.objects.get(id=1)
            Account.objects.create(name=_('Main account'), company=self, currency=eur)
