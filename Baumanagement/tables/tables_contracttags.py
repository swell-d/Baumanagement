from django.urls import reverse
from django.utils.html import format_html

from Baumanagement.models.models_contracts import ContractTag
from Baumanagement.tables.tables import MyTable, modal


class ContractTagTable(MyTable):
    class Meta(MyTable.Meta):
        model = ContractTag
        fields = ContractTag.table_fields

    def render_name(self, record, value):
        return format_html(
            f'''<strong><a href="{modal if self.object_table else reverse('contracttag_id', args=[record.id])}">
            {record}</a></strong>''')
