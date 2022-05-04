from author.decorators import with_author
from django.db import models
from django.db.models import Sum, Case, When
from django.utils.translation import gettext_lazy as _

from companies.models import Company
from main.models import BaseModel, AddressModel, FileModel
from projects.models_labels import ProjectLabel


@with_author
class Project(BaseModel, AddressModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Project name'), unique=True)
    code = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Code'))
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='projects')
    label = models.ManyToManyField(ProjectLabel, blank=True, verbose_name=_('Labels'), related_name='projects')

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(count_contracts=Sum(Case(When(contracts__open=True, then=1))))

    urls = 'projects'
    url_id = 'project_id'
    table_fields = 'created', 'company', 'name', 'code', 'label', 'address', 'count_contracts', 'files'
    search_fields = 'company__name', 'name', 'code', 'address', 'city', 'land', 'count_contracts'
    form_fields = 'open', 'company', 'name', 'code', 'label', 'address', 'city', 'land'
