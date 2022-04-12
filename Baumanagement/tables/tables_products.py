import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_products import Product
from Baumanagement.tables.tables import Files, MyTable, modal


class ProductTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Product
        fields = Product.table_fields

    files = tables.Column(verbose_name=_('Files'))

    def render_name(self, record, value):
        link = reverse('product_id', args=[record.id])
        return format_html(f'<a href="{modal if self.object_table else link}">{value}</a>')

    def render_code(self, record, value):
        link = reverse('product_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_amount_netto_positiv(self, record, value):
        link = reverse('product_id', args=[record.id])
        symbol = record.currency.symbol
        return format_html(
            f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value:.2f} {symbol}</a>''')

    def render_vat(self, record, value):
        link = reverse('product_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_amount_brutto_positiv(self, record, value):
        link = reverse('product_id', args=[record.id])
        symbol = record.currency.symbol
        return format_html(
            f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value:.2f} {symbol}</a>''')
