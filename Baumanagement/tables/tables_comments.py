import django_tables2 as tables

from Baumanagement.models.models_comments import Comment
from Baumanagement.tables.tables import Files, TableDesign


class CommentTable(tables.Table, Files):
    class Meta(TableDesign):
        model = Comment
        fields = Comment.table_fields
