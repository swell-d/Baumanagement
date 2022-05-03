from author.decorators import with_author
from django.db import models
from django.db.models import TextField
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel, PriceModel, FileModel
from Baumanagement.models.models_currency import Currency


@with_author
class ProductCategory(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    parent = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True,
                               verbose_name=_('Classify category under'), related_name='children')

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

    urls = 'productcategories'
    url_id = 'productcategory_id'
    table_fields = 'name',
    search_fields = 'name',
    form_fields = 'name', 'parent'


@with_author
class Product(BaseModel, FileModel, PriceModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    code = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Code'))
    description = TextField(null=False, blank=True, verbose_name=_('Description'))
    currency = models.ForeignKey(Currency, null=False, blank=False, verbose_name=_('Currency'),
                                 on_delete=models.RESTRICT, related_name='products', default=Currency.get_EUR_id)
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

    urls = 'products'
    url_id = 'product_id'
    table_fields = 'type', 'name', 'code', 'categories', 'files', 'amount_netto_positiv', 'vat', 'amount_brutto_positiv'
    search_fields = 'type', 'name', 'code', 'amount_netto_positiv', 'vat', 'amount_brutto_positiv'
    form_fields = 'open', 'type', 'name', 'code', 'description', 'categories', 'currency', 'amount_netto_positiv', 'vat'
