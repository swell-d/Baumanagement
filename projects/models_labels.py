from author.decorators import with_author
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel, Label


@with_author
class ProjectLabel(Label, BaseModel):
    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @property
    def count(self):
        return self.projects.count()

    urls = 'projectlabels'
    url_id = 'projectlabel_id'
    table_fields = 'path',
    search_fields = 'path',
    form_fields = 'name', 'parent'
