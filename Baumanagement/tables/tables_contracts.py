import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_contracts import Contract
from Baumanagement.tables.tables import Files, SummingColumn2F, MyTable, format_amount, get_link, base_render, \
    date_render


class ContractTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Contract
        fields = Contract.table_fields

    amount_netto = SummingColumn2F(verbose_name=_('Amount netto'))
    amount_brutto = SummingColumn2F(verbose_name=_('Amount brutto'))
    bills_amount = SummingColumn2F(verbose_name=_('Bills'))
    payments_amount = SummingColumn2F(verbose_name=_('Payments'))
    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_project(self, record, value):
        link = reverse('project_id', args=[record.project.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.company.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_date(self, record, value):
        return date_render(self, record, value)

    def render_amount_netto(self, record, value):
        return format_amount(value, get_link(record), record.currency.symbol)

    def render_vat(self, record, value):
        return base_render(self, record, value)

    def render_amount_brutto(self, record, value):
        return format_amount(value, get_link(record), record.currency.symbol)

    def render_bills_amount(self, record, value):
        link = reverse('contract_id_bills', args=[record.id])
        return format_amount(value, link, record.currency.symbol)

    def render_payments_amount(self, record, value):
        link = reverse('contract_id_payments', args=[record.id])
        return format_amount(value, link, record.currency.symbol)
