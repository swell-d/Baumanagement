import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_projects import Project
from Baumanagement.tables.tables import Files, SummingColumnInt, get_google_maps_link, MyTable, base_render


class ProjectTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Project
        fields = Project.table_fields

    count_contracts = SummingColumnInt(verbose_name=_('Contracts'))
    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.company.id])
        return format_html(f'<a href="{link}">{value}🔗</a>')

    def render_code(self, record, value):
        return base_render(self, record, value)

    def render_tag(self, record, value):
        return base_render(self, record, value)

    def render_address(self, record, value):
        return get_google_maps_link(record)

    def render_count_contracts(self, record, value):
        link = reverse('project_id_contracts', args=[record.id])
        return format_html(f'<a href="{link}">{value}</a>')
