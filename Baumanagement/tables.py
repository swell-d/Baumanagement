import re
import urllib.parse

import django_tables2 as tables
from django.utils.html import format_html

from .models import Company, Project, Contract, Payment, Bill


def get_google_maps_link(record):
    return format_html(
        f'<a href="https://www.google.de/maps/search/{urllib.parse.quote_plus(record.address + " " + record.city)}" '
        f'target="_blank">{record.address}, {record.city}</a>')


class TableDesign:
    empty_text = "Keine Ergebnisse gefunden"
    template_name = "django_tables2/bootstrap4.html"
    attrs = {'class': 'table table-hover',
             'thead': {'class': 'thead-dark'}}


class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)


class CompanyTable(tables.Table):
    class Meta(TableDesign):
        model = Company
        fields = Company.fields()

    def render_name(self, record):
        return format_html(f'<a href="/company/{record.id}">{record}</a>')

    def render_address(self, record):
        return get_google_maps_link(record)

    def render_phone(self, value):
        return format_html(f'<a href="tel:{re.sub("[^0-9+]", "", value)}">{value}</a>')

    def render_role(self, value):
        return format_html(", ".join([f'<a href="/companies/{role.id}">{role}</a>' for role in value.all()]))


class ProjectTable(tables.Table):
    class Meta(TableDesign):
        model = Project
        fields = Project.fields()

    count_contracts = SummingColumn(orderable=False, verbose_name='Aufträge')

    def render_name(self, record):
        return format_html(f'<a href="/project/{record.id}">{record}</a>')

    def render_code(self, record):
        return format_html(f'<a href="/project/{record.id}">{record.code}</a>')

    def render_company(self, record):
        return format_html(f'<a href="/company/{record.company.id}">{record.company}</a>')

    def render_address(self, record):
        return get_google_maps_link(record)

    def render_count_contracts(self, record, value):
        return format_html(f'<a href="/project/{record.id}">{value}</a>')


class ContractTable(tables.Table):
    class Meta(TableDesign):
        model = Contract
        fields = Contract.fields()

    amount = SummingColumn()
    due = SummingColumn(orderable=False, verbose_name='Rechnungen')
    payed = SummingColumn(orderable=False, verbose_name='Bezahlt')

    def render_project(self, record):
        return format_html(f'<a href="/project/{record.project.id}">{record.project}</a>')

    def render_name(self, record):
        return format_html(f'<a href="/contract/{record.id}">{record}</a>')

    def render_company(self, record):
        return format_html(f'<a href="/company/{record.company.id}">{record.company}</a>')

    def render_due(self, record, value):
        return format_html(f'<a href="/contract/{record.id}/bills">{value}</a>')

    def render_payed(self, record, value):
        return format_html(f'<a href="/contract/{record.id}/payments">{value}</a>')


class PaymentTable(tables.Table):
    amount = SummingColumn()

    class Meta(TableDesign):
        model = Payment
        fields = Payment.fields()

    def render_name(self, record):
        return format_html(f'<a href="/payment/{record.id}">{record}</a>')

    def render_contract(self, record):
        return format_html(f'<a href="/contract/{record.contract.id}">{record.contract}</a>')


class BillTable(tables.Table):
    amount = SummingColumn()

    class Meta(TableDesign):
        model = Bill
        fields = Bill.fields()

    def render_name(self, record):
        return format_html(f'<a href="/bill/{record.id}">{record}</a>')

    def render_contract(self, record):
        return format_html(f'<a href="/contract/{record.contract.id}">{record.contract}</a>')
