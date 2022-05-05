from django.db import models
from django.utils.translation import gettext_lazy as _

from contracts.models import Contract
from main.models import PriceModel
from products.models import Product


class ContractProduct(PriceModel):
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name=_('Contract'),
                                 on_delete=models.RESTRICT, related_name='products')
    product = models.ForeignKey(Product, null=False, blank=False, verbose_name=_('Product'),
                                on_delete=models.RESTRICT)
    count = models.FloatField(null=False, blank=False, verbose_name=_('Count'), default=1.0)
    use_product_price = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.contract.name} :: {self.product.name}'
