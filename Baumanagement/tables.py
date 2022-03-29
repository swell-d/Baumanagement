import re
import urllib.parse

import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Company, Project, Contract, Payment, Bill


def get_google_maps_link(record):
    link = urllib.parse.quote_plus(record.address + " " + record.city + " " + record.land)
    text = f'{record.address}, {record.city}'
    if record.land != 'Deutschland':
        text += f', {record.land}'
    return format_html(f'<a href="https://www.google.de/maps/search/{link}" target="_blank">{text}</a>')


class TableDesign:
    empty_text = _("No results found")
    template_name = "django_tables2/bootstrap4.html"
    attrs = {'class': 'table table-hover'}
    row_attrs = {"class": lambda record: "text-muted" if not record.open else ""}


class SummingColumn2F(tables.Column):
    def render_footer(self, bound_column, table):
        return f'{sum(bound_column.accessor.resolve(row) or 0 for row in table.data if row.open): .2f}'


class SummingColumnInt(tables.Column):
    def render_footer(self, bound_column, table):
        return f'{sum(bound_column.accessor.resolve(row) or 0 for row in table.data): .0f}'


class CreateFooter(tables.Column):
    def render_footer(self):
        return ''


class Files:
    def render_files(self, record):
        files = record.files
        text = ''.join([f'<a href="{each.file.url}" target="_blank">{str(each)[str(each).rfind(".") + 1:].upper()}</a>'
                        for each in files[:1]])
        if len(files) > 1:
            text = f'''
<div class="dropdown">
    {text}
    <a class="btn btn-outline-secondary btn-sm ms-2" href="#" role="button" 
    id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false">
        +{len(files) - 1}
    </a>
    <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
        {''.join([f'<li><a class="dropdown-item" href="{each.file.url}" target="_blank">{str(each)}</a></li>'
                  for each in files])}
    </ul>
</div>'''
        return format_html(text)


class CompanyTable(tables.Table, Files):
    class Meta(TableDesign):
        model = Company
        fields = Company.table_fields()

    name = CreateFooter()
    files = tables.Column(verbose_name=_('Files'))

    def render_name(self, record, value):
        link = reverse('company_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_address(self, record, value):
        return get_google_maps_link(record)

    def render_phone(self, record, value):
        return format_html(f'<a href="tel:{re.sub("[^0-9+]", "", value)}">{value}</a>')

    def render_role(self, record, value):
        def role_link(role):
            return reverse('companies_id', args=[role.id])

        return format_html(", ".join([f'<a href="{role_link(role)}">{role}</a>' for role in value.all()]))


class ProjectTable(tables.Table, Files):
    class Meta(TableDesign):
        model = Project
        fields = Project.table_fields()

    count_contracts = SummingColumnInt(verbose_name=_('Contracts'))
    files = tables.Column(verbose_name=_('Files'))

    def render_created(self, record, value):
        link = reverse('project_id', args=[record.id])
        return format_html(f'<a href="{link}">{value.strftime("%d.%m.%Y %H:%M")}</a>')

    def render_name(self, record, value):
        link = reverse('project_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_code(self, record, value):
        link = reverse('project_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.company.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_address(self, record, value):
        return get_google_maps_link(record)

    def render_count_contracts(self, record, value):
        link = reverse('project_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')


class ContractTable(tables.Table, Files):
    class Meta(TableDesign):
        model = Contract
        fields = Contract.table_fields()

    amount_netto = SummingColumn2F()
    amount_brutto = SummingColumn2F()
    due = SummingColumn2F(verbose_name=_('Bills'))
    payed = SummingColumn2F(verbose_name=_('Payments'))
    files = tables.Column(verbose_name=_('Files'))

    def render_created(self, record, value):
        link = reverse('contract_id', args=[record.id])
        return format_html(f'<a href="{link}">{value.strftime("%d.%m.%Y %H:%M")}</a>')

    def render_project(self, record, value):
        link = reverse('project_id', args=[record.project.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.company.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_name(self, record, value):
        link = reverse('contract_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_date(self, record, value):
        link = reverse('contract_id', args=[record.id])
        return format_html(f'<a href="{link}">{value.strftime("%d.%m.%Y")}</a>')

    def render_amount_netto(self, record, value):
        link = reverse('contract_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_vat(self, record, value):
        link = reverse('contract_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_amount_brutto(self, record, value):
        link = reverse('contract_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_due(self, record, value):
        link = reverse('contract_id_bills', args=[record.id])
        return format_html(f'<a href="{link}">{value:.2f}</a>')

    def render_payed(self, record, value):
        link = reverse('contract_id_payments', args=[record.id])
        return format_html(f'<a href="{link}">{value:.2f}</a>')


class BillTable(tables.Table, Files):
    class Meta(TableDesign):
        model = Bill
        fields = Bill.table_fields()

    project = tables.Column(verbose_name=_('Project'))
    company = tables.Column(verbose_name=_('Company'))
    amount_netto = SummingColumn2F()
    amount_brutto = SummingColumn2F()
    files = tables.Column(verbose_name=_('Files'))

    def render_created(self, record, value):
        link = reverse('bill_id', args=[record.id])
        return format_html(f'<a href="{link}">{value.strftime("%d.%m.%Y %H:%M")}</a>')

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
        return format_html(f'<a href="{link}">{value}</a>')

    def render_date(self, record, value):
        link = reverse('bill_id', args=[record.id])
        return format_html(f'<a href="{link}">{value.strftime("%d.%m.%Y")}</a>')

    def render_amount_netto(self, record, value):
        link = reverse('bill_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_vat(self, record, value):
        link = reverse('bill_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_amount_brutto(self, record, value):
        link = reverse('bill_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')


class PaymentTable(tables.Table, Files):
    class Meta(TableDesign):
        model = Payment
        fields = Payment.table_fields()

    project = tables.Column(verbose_name=_('Project'))
    company = tables.Column(verbose_name=_('Company'))
    amount_netto = SummingColumn2F()
    amount_brutto = SummingColumn2F()
    files = tables.Column(verbose_name=_('Files'))

    def render_created(self, record, value):
        link = reverse('payment_id', args=[record.id])
        return format_html(f'<a href="{link}">{value.strftime("%d.%m.%Y %H:%M")}</a>')

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
        link = reverse('payment_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_date(self, record, value):
        link = reverse('payment_id', args=[record.id])
        return format_html(f'<a href="{link}">{value.strftime("%d.%m.%Y")}</a>')

    def render_amount_netto(self, record, value):
        link = reverse('payment_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_vat(self, record, value):
        link = reverse('payment_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_amount_brutto(self, record, value):
        link = reverse('payment_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')
