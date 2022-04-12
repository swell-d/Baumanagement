from Baumanagement.models.models_company import CompanyRole
from Baumanagement.tables.tables import MyTable


class CompanyRoleTable(MyTable):
    class Meta(MyTable.Meta):
        model = CompanyRole
        fields = CompanyRole.table_fields
