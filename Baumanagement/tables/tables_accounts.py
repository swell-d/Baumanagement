from decimal import Decimal

import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Account
from Baumanagement.tables.tables import Files, MyTable, modal


class AccountTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Account
        fields = Account.table_fields

    files = tables.Column(verbose_name=_('Files'))
    balance = tables.Column(accessor=tables.A("pk"), verbose_name=_('Balance'))  # Kontostand

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.company.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_name(self, record, value):
        link = reverse('account_id', args=[record.id])
        return format_html(f'<a href="{modal if self.object_table else link}">{value}</a>')

    def render_currency(self, record, value):
        link = reverse('account_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_IBAN(self, record, value):
        link = reverse('account_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_BIC(self, record, value):
        link = reverse('account_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_balance(self, record):
        link = reverse('account_id_payments', args=[record.id])
        value = -(record.sum1 or Decimal(0)) + (record.sum2 or Decimal(0))
        symbol = record.currency.symbol
        return format_html(
            f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value:.2f} {symbol}</a>''')
