from django.urls import reverse
from django.utils.html import format_html

from Baumanagement.models.models_company import CompanyRole
from Baumanagement.tables.tables import MyTable, modal


class CompanyRoleTable(MyTable):
    class Meta(MyTable.Meta):
        model = CompanyRole
        fields = CompanyRole.table_fields

    def render_name(self, record, value):
        return format_html(
            f'''<a href="{modal if self.object_table else reverse('companyrole_id', args=[record.id])}">{value}</a>''')
