from django.db import models
from django.db.models import Sum, Case, When
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.abstract import BaseModel, AddressModel, FileModel
from Baumanagement.models.models_company import Company


class ProjectRole(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Role'))

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @property
    def count_projects(self):
        return self.companies.count()

    url = 'projectroles'
    table_fields = 'name',
    search_fields = 'name',
    form_fields = 'name',


class Project(BaseModel, AddressModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Project name'))
    code = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Code'))
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='projects')
    role = models.ForeignKey(ProjectRole, blank=False, verbose_name=_('Role'), on_delete=models.RESTRICT,
                             related_name='projects')

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(count_contracts=Sum(Case(When(contracts__open=True, then=1))))

    url = 'projects'
    table_fields = 'created', 'company', 'name', 'code', 'role', 'address', 'count_contracts', 'files'
    search_fields = 'company__name', 'name', 'code', 'role__name', 'address', 'city', 'land', 'count_contracts'
    form_fields = 'open', 'company', 'name', 'code', 'role', 'address', 'city', 'land'