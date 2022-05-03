import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_products import Product
from main.tables import Files, MyTable, base_render


class ProductTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Product
        fields = Product.table_fields

    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_type(self, record, value):
        return base_render(self, record, value)

    def render_categories(self, record, value):
        return format_html(
            "<br>".join([f'<a href="{reverse("product_id", args=[record.id])}">{cat}</a>' for cat in value.all()]))
