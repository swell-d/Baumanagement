import re

import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Company
from Baumanagement.tables.tables import Files, get_google_maps_link, MyTable


class CompanyTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Company
        fields = Company.table_fields

    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_address(self, record, value):
        return get_google_maps_link(record)

    def render_phone(self, record, value):
        return format_html(f'<a href="tel:{re.sub("[^0-9+]", "", value)}">{value}</a>')

    def render_role(self, record, value):
        return format_html(
            ", ".join([f'<a href="{reverse("company_id", args=[record.id])}">{role}</a>' for role in value.all()]))
