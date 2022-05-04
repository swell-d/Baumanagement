from author.decorators import with_author
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel, Label


@with_author
class ProductCategory(Label, BaseModel):
    parent = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True,
                               verbose_name=_('Classify category under'), related_name='children')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    @property
    def count(self):
        return self.products.count()

    urls = 'productcategories'
    url_id = 'productcategory_id'
    table_fields = 'path',
    search_fields = 'path',
    form_fields = 'name', 'parent'
