import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_contracts import Contract
from Baumanagement.tables.tables import Files, SummingColumn2F, MyTable, modal


class ContractTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Contract
        fields = Contract.table_fields

    amount_netto = SummingColumn2F(verbose_name=_('Amount netto'))
    amount_brutto = SummingColumn2F(verbose_name=_('Amount brutto'))
    due = SummingColumn2F(verbose_name=_('Bills'))
    payed = SummingColumn2F(verbose_name=_('Payments'))
    files = tables.Column(verbose_name=_('Files'))

    def render_project(self, record, value):
        link = reverse('project_id', args=[record.project.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.company.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_name(self, record, value):
        link = reverse('contract_id', args=[record.id])
        return format_html(f'<strong><a href="{modal if self.object_table else link}">{value}</a></strong>')

    def render_date(self, record, value):
        link = reverse('contract_id', args=[record.id])
        return format_html(f'<a href="{link}">{value.strftime("%d.%m.%Y") if value else "—"}</a>')

    def render_amount_netto(self, record, value):
        link = reverse('contract_id', args=[record.id])
        symbol = record.currency.symbol
        return format_html(
            f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value:.2f} {symbol}</a>''')

    def render_vat(self, record, value):
        link = reverse('contract_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_amount_brutto(self, record, value):
        link = reverse('contract_id', args=[record.id])
        symbol = record.currency.symbol
        return format_html(
            f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value:.2f} {symbol}</a>''')

    def render_due(self, record, value):
        link = reverse('contract_id_bills', args=[record.id])
        symbol = record.currency.symbol
        return format_html(
            f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value:.2f} {symbol}</a>''')

    def render_payed(self, record, value):
        link = reverse('contract_id_payments', args=[record.id])
        symbol = record.currency.symbol
        return format_html(
            f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value:.2f} {symbol}</a>''')
