from author.decorators import with_author
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel


@with_author
class CompanyRole(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Role'), unique=True)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @property
    def count(self):
        return self.companies.count()

    urls = 'companyroles'
    url_id = 'companyrole_id'
    table_fields = 'name',
    search_fields = 'name',
    form_fields = 'name',
