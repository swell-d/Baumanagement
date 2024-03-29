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

    def render_count_contracts(self, record, value):
        link = reverse('project_id_contracts', args=[record.id])
        return format_html(f'<a href="{link}">{value} &#8694;</a>')
