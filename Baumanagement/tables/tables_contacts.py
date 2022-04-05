import re

import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Contact
from Baumanagement.tables.tables import Files, TableDesign


class ContactTable(tables.Table, Files):
    class Meta(TableDesign):
        model = Contact
        fields = Contact.table_fields

    files = tables.Column(verbose_name=_('Files'), footer="")

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.company.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_name(self, record, value):
        link = reverse('contact_id', args=[record.id])
        return format_html(f'<strong><a href="{link}">{value}</a></strong>')

    def render_phone(self, record, value):
        return format_html(f'<a href="tel:{re.sub("[^0-9+]", "", value)}">{value}</a>')

    def render_position(self, record, value):
        link = reverse('contact_id', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')
