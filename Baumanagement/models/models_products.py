from django.db import models
from django.db.models import TextField
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.abstract import BaseModel, FileModel, PriceModel
from Baumanagement.models.models_company import Currency


class Product(BaseModel, FileModel, PriceModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    code = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Code'))
    description = TextField(null=False, blank=True, verbose_name=_('Description'))
    currency = models.ForeignKey(Currency, null=False, blank=False, verbose_name=_('Currency'),
                                 on_delete=models.RESTRICT, related_name='products')

    PRODUCT = 'Product'
    SERVICE = 'Service'
    TYPE_CHOISES = [
        (PRODUCT, _('Product')),
        (SERVICE, _('Service')),
    ]
    type = models.CharField(max_length=7, choices=TYPE_CHOISES,
                            default=PRODUCT, verbose_name=_('Product type'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    url = 'products'
    table_fields = 'created', 'type', 'name', 'code', 'files', 'amount_netto_positiv', 'vat', 'amount_brutto_positiv'
    search_fields = 'name', 'type', 'code', 'amount_netto_positiv', 'vat', 'amount_brutto_positiv'
    form_fields = 'open', 'type', 'name', 'code', 'description', 'currency', 'amount_netto_positiv', 'vat'
