import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_contracts import Payment
from Baumanagement.tables.tables import Files, SummingColumn2F, MyTable


class PaymentTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Payment
        fields = Payment.table_fields

    project = tables.Column(verbose_name=_('Project'))
    company = tables.Column(verbose_name=_('Company'))
    amount_netto = SummingColumn2F(verbose_name=_('Amount netto'))
    amount_brutto = SummingColumn2F(verbose_name=_('Amount brutto'))
    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_project(self, record, value):
        link = reverse('project_id', args=[record.contract.project.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_contract(self, record, value):
        link = reverse('contract_id', args=[record.contract.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.contract.company.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_date(self, record, value):
        link = reverse('payment_id', args=[record.id])
        return format_html(f'<a href="{link}">{value.strftime("%d.%m.%Y") if value else "—"}</a>')

    def render_amount_netto(self, record, value):
        link = reverse('payment_id', args=[record.id])
        symbol = record.currency.symbol
        return format_html(
            f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value:.2f} {symbol}</a>''')

    def render_vat(self, record, value):
        link = reverse('payment_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_amount_brutto(self, record, value):
        link = reverse('payment_id', args=[record.id])
        symbol = record.currency.symbol
        return format_html(
            f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value:.2f} {symbol}</a>''')
