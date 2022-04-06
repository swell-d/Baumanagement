import datetime

from django.db import models
from django.db.models import Sum, F, Case, When
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.abstract import BaseModel, AddressModel, FileModel, PriceModel
from Baumanagement.models.models_company import Company, Currency, Account


class Project(BaseModel, AddressModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Project name'))
    code = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Code'))
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='projects')

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(count_contracts=Sum(Case(When(contracts__open=True, then=1))))

    table_fields = 'created', 'company', 'name', 'code', 'address', 'count_contracts', 'files'
    search_fields = 'company__name', 'name', 'code', 'address', 'city', 'land', 'count_contracts'
    form_fields = 'open', 'company', 'name', 'code', 'address', 'city', 'land'


class Contract(BaseModel, PriceModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Contract name'))
    date = models.DateField(null=True, blank=True, verbose_name=_('Date'), default=datetime.date.today)
    project = models.ForeignKey(Project, null=False, blank=False, verbose_name=_('Project'),
                                on_delete=models.RESTRICT, related_name='contracts')
    currency = models.ForeignKey(Currency, null=False, blank=False, verbose_name=_('Currency'),
                                 on_delete=models.RESTRICT, related_name='contracts')
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='contracts')
    BUY = PriceModel.BUY
    SELL = PriceModel.SELL
    TYPE_CHOISES = PriceModel.TYPE_CHOISES
    type = models.CharField(max_length=4, choices=TYPE_CHOISES,
                            default=PriceModel.BUY, verbose_name=_('Contract type'))

    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(payed=Sum(Case(When(payments__open=True, then='payments__amount_brutto')), distinct=True)) \
            .annotate(due=Sum(Case(When(bills__open=True, then='bills__amount_brutto')), distinct=True))

    table_fields = 'created', 'project', 'company', 'name', 'date', 'files', 'type', 'amount_netto', 'vat', 'amount_brutto', 'due', 'payed'
    search_fields = 'project__name', 'company__name', 'type', 'name', 'amount_netto', 'vat', 'amount_brutto', 'due', 'payed'
    form_fields = 'open', 'project', 'company', 'type', 'name', 'date', 'currency', 'amount_netto_positiv', 'vat'


class Bill(BaseModel, PriceModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Bill name'))
    date = models.DateField(null=True, blank=True, verbose_name=_('Date'), default=datetime.date.today)
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name=_('Contract'),
                                 on_delete=models.RESTRICT, related_name='bills')

    class Meta:
        verbose_name = _('Bill')
        verbose_name_plural = _('Bills')

    @property
    def type(self):
        return self.contract.type

    @property
    def currency(self):
        return self.contract.currency

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(project=F('contract__project__name'), company=F('contract__company__name'),
                           type1=F('contract__type'))

    table_fields = 'created', 'project', 'company', 'contract', 'name', 'date', 'files', 'type1', 'amount_netto', 'vat', 'amount_brutto'
    search_fields = 'project', 'company', 'contract__name', 'name', 'amount_netto', 'vat', 'amount_brutto'
    form_fields = 'open', 'contract', 'name', 'date', 'amount_netto_positiv', 'vat'


class Payment(BaseModel, PriceModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Payment name'))
    date = models.DateField(null=True, blank=True, verbose_name=_('Date'), default=datetime.date.today)
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name=_('Contract'),
                                 on_delete=models.RESTRICT, related_name='payments')
    account_from = models.ForeignKey(Account, null=False, blank=False, verbose_name=_('Write-off account'),
                                     on_delete=models.RESTRICT, related_name='bills_from')
    account_to = models.ForeignKey(Account, null=False, blank=False, verbose_name=_('Top-up account'),
                                   on_delete=models.RESTRICT, related_name='bills_to')

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    @property
    def type(self):
        return self.contract.type

    @property
    def currency(self):
        return self.contract.currency

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(project=F('contract__project__name'), company=F('contract__company__name'),
                           type1=F('contract__type'))

    table_fields = 'created', 'project', 'company', 'contract', 'name', 'date', 'files', 'type1', 'amount_netto', 'vat', 'amount_brutto'
    search_fields = 'project', 'company', 'contract__name', 'name', 'amount_netto', 'vat', 'amount_brutto'
    form_fields = 'open', 'contract', 'name', 'date', 'account_from', 'account_to', 'amount_netto_positiv', 'vat'
