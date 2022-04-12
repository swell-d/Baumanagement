from django.urls import reverse
from django.utils.html import format_html

from Baumanagement.models.models_company import Currency
from Baumanagement.tables.tables import MyTable


class CurrencyTable(MyTable):
    class Meta(MyTable.Meta):
        model = Currency
        fields = Currency.table_fields

    def render_code(self, record, value):
        link = reverse('currency_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')
