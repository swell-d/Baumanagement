import datetime

from django.db import models
from django.db.models import Sum, F, Case, When
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.abstract import BaseModel, AddressModel, FileModel, PriceModel
from Baumanagement.models.models_company import Company


class Project(BaseModel, AddressModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Project name'))
    code = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Code'))
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='projects')

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(count_contracts=Sum(Case(When(contracts__open=True, then=1))))

    table_fields = 'created', 'company', 'name', 'code', 'address', 'open', 'count_contracts', 'files'
    search_fields = 'company__name', 'name', 'code', 'address', 'city', 'land', 'count_contracts'
    form_fields = 'open', 'company', 'name', 'code', 'address', 'city', 'land'


class Contract(BaseModel, PriceModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Contract name'))
    date = models.DateField(null=False, blank=True, verbose_name=_('Date'), default=datetime.date.today)
    project = models.ForeignKey(Project, null=False, blank=False, verbose_name=_('Project'),
                                on_delete=models.RESTRICT, related_name='contracts')
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='contracts')

    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(payed=Sum(Case(When(payments__open=True, then='payments__amount_brutto')), distinct=True)) \
            .annotate(due=Sum(Case(When(bills__open=True, then='bills__amount_brutto')), distinct=True))

    table_fields = 'created', 'project', 'company', 'name', 'date', 'files', 'amount_netto', 'vat', 'amount_brutto', 'due', 'payed'
    search_fields = 'project__name', 'company__name', 'name', 'amount_netto', 'vat', 'amount_brutto', 'due', 'payed'
    form_fields = 'open', 'project', 'company', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto'


class Bill(BaseModel, PriceModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Bill name'))
    date = models.DateField(null=False, blank=True, verbose_name=_('Date'), default=datetime.date.today)
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name=_('Contract'),
                                 on_delete=models.RESTRICT, related_name='bills')

    class Meta:
        verbose_name = _('Bill')
        verbose_name_plural = _('Bills')

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(project=F('contract__project__name'), company=F('contract__company__name'))

    table_fields = 'created', 'project', 'company', 'contract', 'name', 'date', 'files', 'amount_netto', 'vat', 'amount_brutto'
    search_fields = 'project', 'company', 'contract__name', 'name', 'amount_netto', 'vat', 'amount_brutto'
    form_fields = 'open', 'contract', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto'


class Payment(BaseModel, PriceModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Payment name'))
    date = models.DateField(null=False, blank=True, verbose_name=_('Date'), default=datetime.date.today)
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name=_('Contract'),
                                 on_delete=models.RESTRICT, related_name='payments')

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(project=F('contract__project__name'), company=F('contract__company__name'))

    table_fields = 'created', 'project', 'company', 'contract', 'name', 'date', 'files', 'amount_netto', 'vat', 'amount_brutto'
    search_fields = 'project', 'company', 'contract__name', 'name', 'amount_netto', 'vat', 'amount_brutto'
    form_fields = 'open', 'contract', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto'
