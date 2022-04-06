import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Bill
from Baumanagement.tables.tables import Files, SummingColumn2F, MyTable


class BillTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Bill
        fields = Bill.table_fields

    project = tables.Column(verbose_name=_('Project'))
    company = tables.Column(verbose_name=_('Company'))
    amount_netto = SummingColumn2F()
    amount_brutto = SummingColumn2F()
    files = tables.Column(verbose_name=_('Files'))
    type1 = tables.Column(verbose_name=_('Type'))

    def render_project(self, record, value):
        link = reverse('project_id', args=[record.contract.project.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_contract(self, record, value):
        link = reverse('contract_id', args=[record.contract.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.contract.company.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_name(self, record, value):
        link = reverse('bill_id', args=[record.id])
        return format_html(f'<strong><a href="{link}">{value}</a></strong>')

    def render_date(self, record, value):
        link = reverse('bill_id', args=[record.id])
        return format_html(f'<a href="{link}">{value.strftime("%d.%m.%Y")}</a>')

    def render_type1(self, record, value):
        return record.contract.get_type_display()

    def render_amount_netto(self, record, value):
        link = reverse('bill_id', args=[record.id])
        symbol = record.currency.symbol
        return format_html(f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value} {symbol}</a>''')

    def render_vat(self, record, value):
        link = reverse('bill_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_amount_brutto(self, record, value):
        link = reverse('bill_id', args=[record.id])
        symbol = record.currency.symbol
        return format_html(f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value} {symbol}</a>''')
