from Baumanagement.models.models_contracts import ContractTag
from Baumanagement.tables.tables import MyTable


class ContractTagTable(MyTable):
    class Meta(MyTable.Meta):
        model = ContractTag
        fields = ContractTag.table_fields
