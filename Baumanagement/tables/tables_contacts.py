import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Contact
from Baumanagement.tables.tables import Files, MyTable, base_render


class ContactTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Contact
        fields = Contact.table_fields

    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_position(self, record, value):
        return base_render(self, record, value)
