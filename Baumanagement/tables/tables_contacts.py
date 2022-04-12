import re

import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Contact
from Baumanagement.tables.tables import Files, MyTable, base_render


class ContactTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Contact
        fields = Contact.table_fields

    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.company.id])
        return format_html(f'<a href="{link}">{value}</a>')

    def render_phone(self, record, value):
        return format_html(f'<a href="tel:{re.sub("[^0-9+]", "", value)}">{value}</a>')

    def render_position(self, record, value):
        return base_render(self, record, value)
