import datetime

from django.db import models
from django.db.models import Sum, F, Case, When
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.abstract import BaseModel, AddressModel, PriceModel


class CompanyRole(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Role'))

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    @property
    def count_companies(self):
        return self.companies.count()


class Company(BaseModel, AddressModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Company name'))
    email = models.EmailField(null=False, blank=True, verbose_name=_('E-mail'))
    phone = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Phone'))
    role = models.ManyToManyField(CompanyRole, blank=False, verbose_name=_('Role'), related_name='companies')
    ceo = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('CEO'))
    vat_number = models.CharField(max_length=16, null=False, blank=True, verbose_name=_('VAT number'))

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @staticmethod
    def table_fields():
        return 'name', 'address', 'email', 'phone', 'role', 'ceo', 'vat_number', 'files'

    @staticmethod
    def search_fields():
        return 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number'

    @staticmethod
    def form_fields():
        return 'open', 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number', 'role'


class Project(BaseModel, AddressModel):
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

    @staticmethod
    def table_fields():
        return 'created', 'name', 'code', 'company', 'address', 'open', 'count_contracts', 'files'

    @staticmethod
    def search_fields():
        return 'name', 'code', 'company__name', 'address', 'city', 'land', 'count_contracts'

    @staticmethod
    def form_fields():
        return 'open', 'name', 'code', 'company', 'address', 'city', 'land'


class Contract(BaseModel, PriceModel):
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

    @staticmethod
    def table_fields():
        return 'created', 'project', 'company', 'name', 'date', 'files', 'amount_netto', 'vat', 'amount_brutto', 'due', 'payed'

    @staticmethod
    def search_fields():
        return 'project__name', 'company__name', 'name', 'amount_netto', 'vat', 'amount_brutto', 'due', 'payed'

    @staticmethod
    def form_fields():
        return 'open', 'project', 'company', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto'


class Bill(BaseModel, PriceModel):
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

    @staticmethod
    def table_fields():
        return 'created', 'project', 'company', 'contract', 'name', 'date', 'files', 'amount_netto', 'vat', 'amount_brutto'

    @staticmethod
    def search_fields():
        return 'project', 'company', 'contract__name', 'name', 'amount_netto', 'vat', 'amount_brutto'

    @staticmethod
    def form_fields():
        return 'open', 'contract', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto'


class Payment(BaseModel, PriceModel):
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

    @staticmethod
    def table_fields():
        return 'created', 'project', 'company', 'contract', 'name', 'date', 'files', 'amount_netto', 'vat', 'amount_brutto'

    @staticmethod
    def search_fields():
        return 'project', 'company', 'contract__name', 'name', 'amount_netto', 'vat', 'amount_brutto'

    @staticmethod
    def form_fields():
        return 'open', 'contract', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto'
