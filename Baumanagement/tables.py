import django_tables2 as tables
from django.utils.html import format_html

from .models import Company, CompanyRole


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

    anzahl = tables.Column(empty_values=())

    def render_name(self, value, record):
        return format_html(f'<a href="/role/{record.id}">{value}</a>')

    def render_anzahl(self, record):
        return Company.objects.filter(role=record.id).count()
