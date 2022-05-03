from author.decorators import with_author
from django.db import models
from django.db.models import Sum, Case, When
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel, AddressModel, FileModel
from Baumanagement.models.models_company import Company


@with_author
class ProjectLabel(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    parent = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True,
                               verbose_name=_('Classify label under'), related_name='children')

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')

    def __str__(self):
        return f'{self.parent}/{self.name}' if self.parent else self.name

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @property
    def count(self):
        return self.projects.count()

    urls = 'projectlabels'
    url_id = 'projectlabel_id'
    table_fields = 'name',
    search_fields = 'name',
    form_fields = 'name', 'parent'


@with_author
class Project(BaseModel, AddressModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Project name'), unique=True)
    code = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Code'))
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='projects')
    label = models.ForeignKey(ProjectLabel, blank=False, verbose_name=_('Label'),
                            on_delete=models.RESTRICT, related_name='projects')

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(count_contracts=Sum(Case(When(contracts__open=True, then=1))))

    urls = 'projects'
    url_id = 'project_id'
    table_fields = 'created', 'company', 'name', 'code', 'label', 'address', 'count_contracts', 'files'
    search_fields = 'company__name', 'name', 'code', 'label__name', 'address', 'city', 'land', 'count_contracts'
    form_fields = 'open', 'company', 'name', 'code', 'label', 'address', 'city', 'land'
