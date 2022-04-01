import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Account
from Baumanagement.tables.tables import Files, TableDesign


class AccountTable(tables.Table, Files):
    class Meta(TableDesign):
        model = Account
        fields = Account.table_fields

    files = tables.Column(verbose_name=_('Files'))

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.company.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_name(self, record, value):
        link = reverse('account_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_currency(self, record, value):
        link = reverse('account_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_IBAN(self, record, value):
        link = reverse('account_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_BIC(self, record, value):
        link = reverse('account_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')
