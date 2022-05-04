from author.decorators import with_author
from django.db import models
from django.db.models import TextField
from django.utils.translation import gettext_lazy as _

from currencies.models import Currency
from main.models import BaseModel, FileModel, PriceModel
from products.models_labels import ProductCategory


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
