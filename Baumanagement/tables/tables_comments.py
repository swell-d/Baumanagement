from Baumanagement.models.models_comments import Comment
from Baumanagement.tables.tables import Files, TableDesign, MyTable


class CommentTable(MyTable, Files):
    class Meta(TableDesign):
        model = Comment
        fields = Comment.table_fields
