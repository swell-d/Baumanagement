import urllib.parse

import django_tables2 as tables
from django.utils.html import format_html

from .models import Company, Project, Contract, Payment, Bill


def get_google_maps_link(record):
    return format_html(
        f'<a href="https://www.google.de/maps/search/{urllib.parse.quote_plus(record.address + " " + record.city)}" '
        f'target="_blank">{record.address}, {record.city}</a>')


class CompanyTable(tables.Table):
    class Meta:
        model = Company
        fields = Company.fields()
        empty_text = "Keine Ergebnisse gefunden"
        attrs = {'a': {'text-decoration': 'none;'}}

    def render_name(self, record):
        return format_html(f'<a href="/company/{record.id}">{record}</a>')

    def render_address(self, record):
        return get_google_maps_link(record)

    def render_phone(self, value):
        return format_html(f'<a href="tel:{value}">{value}</a>')

    def render_role(self, value):
        return format_html(", ".join([f'<a href="/companies/{role.id}">{role}</a>' for role in value.all()]))


class ProjectTable(tables.Table):
    class Meta:
        model = Project
        fields = Project.fields()
        empty_text = "Keine Ergebnisse gefunden"

    count_contracts = tables.Column(orderable=False, verbose_name='Aufträge')

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
    class Meta:
        model = Contract
        fields = Contract.fields()
        empty_text = "Keine Ergebnisse gefunden"

    due = tables.Column(orderable=False, verbose_name='Rechnungen')
    payed = tables.Column(orderable=False, verbose_name='Bezahlt')

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
    class Meta:
        model = Payment
        fields = Payment.fields()
        empty_text = "Keine Ergebnisse gefunden"


class BillTable(tables.Table):
    class Meta:
        model = Bill
        fields = Bill.fields()
        empty_text = "Keine Ergebnisse gefunden"
