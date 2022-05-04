import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from main.tables import Files, SummingColumnInt, MyTable
from projects.models import Project


class ProjectTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Project
        fields = Project.table_fields

    count_contracts = SummingColumnInt(verbose_name=_('Contracts'))
    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_label(self, record, value):
        return format_html(
            ", ".join([f'<a href="{reverse(record.url_id, args=[record.id])}" class="badge" style="background-color: '
                       f'{label.color};">{label}</a>' for label in value.all()]))

    def render_count_contracts(self, record, value):
        link = reverse('project_id_contracts', args=[record.id])
        return format_html(f'<a href="{link}">{value} ➡</a>')
