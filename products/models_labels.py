from author.decorators import with_author
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel


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
