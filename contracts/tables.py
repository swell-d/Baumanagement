import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from contracts.models import Contract
from main.tables import Files, SummingColumn2F, MyTable, format_amount


class ContractTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Contract
        fields = Contract.table_fields

    amount_netto = SummingColumn2F(verbose_name=_('Amount netto'))
    amount_brutto = SummingColumn2F(verbose_name=_('Amount brutto'))
    bills_amount = SummingColumn2F(verbose_name=_('Bills'))
    payments_amount = SummingColumn2F(verbose_name=_('Payments'))
    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_label(self, record, value):
        return format_html(
            ", ".join([f'<a href="{reverse(record.url_id, args=[record.id])}">{label}</a>' for label in value.all()]))

    def render_bills_amount(self, record, value):
        link = reverse('contract_id_bills', args=[record.id])
        return format_amount(value, link, record.currency.symbol, arrow=True)

    def render_payments_amount(self, record, value):
        link = reverse('contract_id_payments', args=[record.id])
        return format_amount(value, link, record.currency.symbol, arrow=True)
