import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Company
from Baumanagement.tables.tables import Files, MyTable


class CompanyTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Company
        fields = Company.table_fields

    id = tables.Column(visible=True, verbose_name=_('ID'))
    files = tables.Column(verbose_name=_('Files'), orderable=False)

    def render_role(self, record, value):
        return format_html(
            ", ".join([f'<a href="{reverse("company_id", args=[record.id])}">{role}</a>' for role in value.all()]))
