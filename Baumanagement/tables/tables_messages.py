from Baumanagement.models.models_messages import MyMessage
from Baumanagement.tables.tables import MyTable


class MyMessageTable(MyTable):
    class Meta(MyTable.Meta):
        model = MyMessage
        fields = MyMessage.table_fields

    def render_name(self, record, value):
        return value
