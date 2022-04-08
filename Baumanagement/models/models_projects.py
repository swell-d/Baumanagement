from django.db import models
from django.db.models import Sum, Case, When
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.abstract import BaseModel, AddressModel, FileModel
from Baumanagement.models.models_company import Company


class ProjectType(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Type'))

    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @property
    def count_projects(self):
        return self.projects.count()

    url = 'projecttypes'
    table_fields = 'name',
    search_fields = 'name',
    form_fields = 'name',


class Project(BaseModel, AddressModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Project name'))
    code = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Code'))
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='projects')
    tag = models.ForeignKey(ProjectType, blank=False, verbose_name=_('Type'),
                             on_delete=models.RESTRICT, related_name='projects')

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(count_contracts=Sum(Case(When(contracts__open=True, then=1))))

    url = 'projects'
    table_fields = 'created', 'company', 'name', 'code', 'tag', 'address', 'count_contracts', 'files'
    search_fields = 'company__name', 'name', 'code', 'tag__name', 'address', 'city', 'land', 'count_contracts'
    form_fields = 'open', 'company', 'name', 'code', 'tag', 'address', 'city', 'land'
