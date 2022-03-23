import re
import urllib.parse

import django_tables2 as tables
from django.utils.html import format_html

from .models import Company, Project, Contract, Payment, Bill


def get_google_maps_link(record):
    link = urllib.parse.quote_plus(record.address + " " + record.city + " " + record.land)
    text = f'{record.address}, {record.city}'
    if record.land != 'Deutschland':
        text += f', {record.land}'
    return format_html(f'<a href="https://www.google.de/maps/search/{link}" target="_blank">{text}</a>')


class TableDesign:
    empty_text = "Keine Ergebnisse gefunden"
    template_name = "django_tables2/bootstrap4.html"
    attrs = {'class': 'table table-hover'}


class SummingColumn2F(tables.Column):
    def render_footer(self, bound_column, table):
        return f'{sum(bound_column.accessor.resolve(row) or 0 for row in table.data): .2f}'


class SummingColumnInt(tables.Column):
    def render_footer(self, bound_column, table):
        return f'{sum(bound_column.accessor.resolve(row) or 0 for row in table.data): .0f}'


class CreateFooter(tables.Column):
    def render_footer(self):
        return ''


class CompanyTable(tables.Table):
    class Meta(TableDesign):
        model = Company
        fields = Company.fields()

    name = CreateFooter()

    def render_name(self, record, value):
        return format_html(f'<a href="/company/{record.id}">{value}</a>')

    def render_address(self, record, value):
        return get_google_maps_link(record)

    def render_phone(self, record, value):
        return format_html(f'<a href="tel:{re.sub("[^0-9+]", "", value)}">{value}</a>')

    def render_role(self, record, value):
        return format_html(", ".join([f'<a href="/companies/{role.id}">{role}</a>' for role in value.all()]))


class ProjectTable(tables.Table):
    class Meta(TableDesign):
        model = Project
        fields = Project.fields()

    count_contracts = SummingColumnInt(verbose_name='Aufträge')

    def render_created(self, record, value):
        return format_html(f'<a href="/project/{record.id}">{value.strftime("%d.%m.%Y %H:%M")}</a>')

    def render_name(self, record, value):
        return format_html(f'<a href="/project/{record.id}">{value}</a>')

    def render_code(self, record, value):
        return format_html(f'<a href="/project/{record.id}">{value}</a>')

    def render_company(self, record, value):
        return format_html(f'<a href="/company/{record.company.id}">{value}</a>')

    def render_address(self, record, value):
        return get_google_maps_link(record)

    def render_count_contracts(self, record, value):
        return format_html(f'<a href="/project/{record.id}">{value}</a>')


class ContractTable(tables.Table):
    class Meta(TableDesign):
        model = Contract
        fields = Contract.fields()

    amount_netto = SummingColumn2F()
    amount_brutto = SummingColumn2F()
    due = SummingColumn2F(verbose_name='Rechnungen')
    payed = SummingColumn2F(verbose_name='Zahlungen')

    def render_created(self, record, value):
        return format_html(f'<a href="/contract/{record.id}">{value.strftime("%d.%m.%Y %H:%M")}</a>')

    def render_project(self, record, value):
        return format_html(f'<a href="/project/{record.project.id}">{value}</a>')

    def render_company(self, record, value):
        return format_html(f'<a href="/company/{record.company.id}">{value}</a>')

    def render_name(self, record, value):
        return format_html(f'<a href="/contract/{record.id}">{value}</a>')

    def render_date(self, record, value):
        return format_html(f'<a href="/contract/{record.id}">{value.strftime("%d.%m.%Y")}</a>')

    def render_amount_netto(self, record, value):
        return format_html(f'<a href="/contract/{record.id}">{value}</a>')

    def render_vat(self, record, value):
        return format_html(f'<a href="/contract/{record.id}">{value}</a>')

    def render_amount_brutto(self, record, value):
        return format_html(f'<a href="/contract/{record.id}">{value}</a>')

    def render_due(self, record, value):
        return format_html(f'<a href="/contract/{record.id}/bills">{value:.2f}</a>')

    def render_payed(self, record, value):
        return format_html(f'<a href="/contract/{record.id}/payments">{value:.2f}</a>')


class BillTable(tables.Table):
    class Meta(TableDesign):
        model = Bill
        fields = Bill.fields()

    project = tables.Column(verbose_name='Projekt')
    company = tables.Column(verbose_name='Bearbeiter')
    amount_netto = SummingColumn2F()
    amount_brutto = SummingColumn2F()

    def render_created(self, record, value):
        return format_html(f'<a href="/bill/{record.id}">{value.strftime("%d.%m.%Y %H:%M")}</a>')

    def render_project(self, record, value):
        return format_html(f'<a href="/project/{record.contract.project.id}">{value}</a>')

    def render_contract(self, record, value):
        return format_html(f'<a href="/contract/{record.contract.id}">{value}</a>')

    def render_company(self, record, value):
        return format_html(f'<a href="/company/{record.contract.company.id}">{value}</a>')

    def render_name(self, record, value):
        return format_html(f'<a href="/bill/{record.id}">{value}</a>')

    def render_date(self, record, value):
        return format_html(f'<a href="/bill/{record.id}">{value.strftime("%d.%m.%Y")}</a>')

    def render_amount_netto(self, record, value):
        return format_html(f'<a href="/bill/{record.id}">{value}</a>')

    def render_vat(self, record, value):
        return format_html(f'<a href="/bill/{record.id}">{value}</a>')

    def render_amount_brutto(self, record, value):
        return format_html(f'<a href="/bill/{record.id}">{value}</a>')


class PaymentTable(tables.Table):
    class Meta(TableDesign):
        model = Payment
        fields = Payment.fields()

    project = tables.Column(verbose_name='Projekt')
    company = tables.Column(verbose_name='Bearbeiter')
    amount_netto = SummingColumn2F()
    amount_brutto = SummingColumn2F()

    def render_created(self, record, value):
        return format_html(f'<a href="/payment/{record.id}">{value.strftime("%d.%m.%Y %H:%M")}</a>')

    def render_project(self, record, value):
        return format_html(f'<a href="/project/{record.contract.project.id}">{value}</a>')

    def render_contract(self, record, value):
        return format_html(f'<a href="/contract/{record.contract.id}">{value}</a>')

    def render_company(self, record, value):
        return format_html(f'<a href="/company/{record.contract.company.id}">{value}</a>')

    def render_name(self, record, value):
        return format_html(f'<a href="/payment/{record.id}">{value}</a>')

    def render_date(self, record, value):
        return format_html(f'<a href="/payment/{record.id}">{value.strftime("%d.%m.%Y")}</a>')

    def render_amount_netto(self, record, value):
        return format_html(f'<a href="/payment/{record.id}">{value}</a>')

    def render_vat(self, record, value):
        return format_html(f'<a href="/payment/{record.id}">{value}</a>')

    def render_amount_brutto(self, record, value):
        return format_html(f'<a href="/payment/{record.id}">{value}</a>')
