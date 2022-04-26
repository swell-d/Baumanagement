import django_tables2 as tables
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_contracts import Contract
from Baumanagement.tables.tables import Files, SummingColumn2F, MyTable, format_amount


class ContractTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Contract
        fields = Contract.table_fields

    amount_netto = SummingColumn2F(verbose_name=_('Amount netto'))
    amount_brutto = SummingColumn2F(verbose_name=_('Amount brutto'))
    bills_amount = SummingColumn2F(verbose_name=_('Bills'))
    payments_amount = SummingColumn2F(verbose_name=_('Payments'))
    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_bills_amount(self, record, value):
        link = reverse('contract_id_bills', args=[record.id])
        return format_amount(value, link, record.currency.symbol, arrow=True)

    def render_payments_amount(self, record, value):
        link = reverse('contract_id_payments', args=[record.id])
        return format_amount(value, link, record.currency.symbol, arrow=True)
