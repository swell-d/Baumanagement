import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from Baumanagement.models.models_company import Currency
from Baumanagement.tables.tables import TableDesign


class CurrencyTable(tables.Table):
    class Meta(TableDesign):
        model = Currency
        fields = Currency.table_fields

    def render_name(self, record, value):
        link = reverse('currency_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_code(self, record, value):
        link = reverse('currency_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')
