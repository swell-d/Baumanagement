import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from companies.models import Company
from main.tables import Files, MyTable


class CompanyTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Company
        fields = Company.table_fields

    id = tables.Column(visible=True, verbose_name=_('ID'))
    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_label(self, record, value):
        return format_html(
            ", ".join([f'<a href="{reverse(record.url_id, args=[record.id])}" class="badge" style="background-color: '
                       f'{label.color};">{label}</a>' for label in value.all()]))
