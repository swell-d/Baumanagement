import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_comments import Comment
from Baumanagement.tables.tables import Files, MyTable


class CommentTable(MyTable, Files):
    class Meta(MyTable.Meta):
        model = Comment
        fields = Comment.table_fields

    files = tables.Column(verbose_name=_('Files'), orderable=False)
