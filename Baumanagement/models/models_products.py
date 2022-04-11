from django.db import models
from django.db.models import TextField
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.abstract import BaseModel, FileModel, PriceModel
from Baumanagement.models.models_company import Currency


class ProductCategory(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    parent = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True,
                               verbose_name=_('Classify category under'), related_name='categories')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f'{self.parent}/{self.name}' if self.parent else self.name

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @property
    def count(self):
        return self.products.count()

    url = 'productcategories'
    table_fields = 'name',
    search_fields = 'name',
    form_fields = 'name', 'parent'


class Product(BaseModel, FileModel, PriceModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    code = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Code'))
    description = TextField(null=False, blank=True, verbose_name=_('Description'))
    currency = models.ForeignKey(Currency, null=False, blank=False, verbose_name=_('Currency'),
                                 on_delete=models.RESTRICT, related_name='products')
    categories = models.ManyToManyField(ProductCategory, blank=True, verbose_name=_('Categories'),
                                        related_name='products')

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
    form_fields = 'open', 'type', 'name', 'code', 'description', 'categories', 'currency', 'amount_netto_positiv', 'vat'
