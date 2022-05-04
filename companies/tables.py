import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from companies.models import Company
from main.tables import Files, MyTable


class CompanyTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Company
        fields = Company.table_fields

    id = tables.Column(visible=True, verbose_name=_('ID'))
    files = tables.Column(verbose_name=_('Files'), orderable=False)
