import django_tables2 as tables
from django.utils.html import format_html

from .models import Company, CompanyRole, Project, Contract, Payment


class CompanyTable(tables.Table):
    class Meta:
        model = Company
        fields = Company.fields()

    def render_phone(self, value):
        return format_html(f'<a href="tel:{value}">{value}</a>')

    def render_role(self, value):
        return format_html(", ".join([f'<a href="/role/{role.id}">{role.name}</a>' for role in value.all()]))


class CompanyRoleTable(tables.Table):
    class Meta:
        model = CompanyRole
        fields = CompanyRole.fields()

    # CompanyRole.count_companies()
    count1 = tables.Column(verbose_name='Anzahl')

    def render_name(self, value, record):
        return format_html(f'<a href="/role/{record.id}">{value}</a>')

    def render_count1(self, record):
        return record.count_companies()


class ProjectTable(tables.Table):
    class Meta:
        model = Project
        fields = Project.fields()


class ContractTable(tables.Table):
    class Meta:
        model = Contract
        fields = Contract.fields()

    payments = tables.Column(verbose_name='Bezahlt')

    def render_payments(self, record):
        return record.payed()


class PaymentTable(tables.Table):
    class Meta:
        model = Payment
        fields = Payment.fields()

