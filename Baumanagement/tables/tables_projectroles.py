from django.urls import reverse
from django.utils.html import format_html

from Baumanagement.models.models_projects import ProjectRole
from Baumanagement.tables.tables import MyTable, modal


class ProjectRoleTable(MyTable):
    class Meta(MyTable.Meta):
        model = ProjectRole
        fields = ProjectRole.table_fields

    def render_name(self, record, value):
        return format_html(
            f'''<strong><a href="{modal if self.object_table else reverse('projectrole_id', args=[record.id])}">
            {value}</a></strong>''')
