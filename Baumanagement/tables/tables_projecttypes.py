from django.urls import reverse
from django.utils.html import format_html

from Baumanagement.models.models_projects import ProjectType
from Baumanagement.tables.tables import MyTable, modal


class ProjectTypeTable(MyTable):
    class Meta(MyTable.Meta):
        model = ProjectType
        fields = ProjectType.table_fields

    def render_name(self, record, value):
        return format_html(
            f'''<strong><a href="{modal if self.object_table else reverse('projecttype_id', args=[record.id])}">
            {value}</a></strong>''')
