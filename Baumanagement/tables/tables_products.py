import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_products import Product
from Baumanagement.tables.tables import Files, MyTable, format_amount, get_link, base_render


class ProductTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Product
        fields = Product.table_fields

    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_code(self, record, value):
        return base_render(self, record, value)

    def render_amount_netto_positiv(self, record, value):
        return format_amount(value, get_link(record), record.currency.symbol)

    def render_vat(self, record, value):
        return base_render(self, record, value)

    def render_amount_brutto_positiv(self, record, value):
        return format_amount(value, get_link(record), record.currency.symbol)
