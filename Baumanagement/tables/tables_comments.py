from Baumanagement.models.models_comments import Comment
from Baumanagement.tables.tables import Files, MyTable


class CommentTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Comment
        fields = Comment.table_fields
