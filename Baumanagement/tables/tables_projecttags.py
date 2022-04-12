from Baumanagement.models.models_projects import ProjectTag
from Baumanagement.tables.tables import MyTable


class ProjectTagTable(MyTable):
    class Meta(MyTable.Meta):
        model = ProjectTag
        fields = ProjectTag.table_fields
