from author.decorators import with_author
from django.db import models
from django.db.models import Sum, DecimalField, OuterRef, Subquery, Case, When
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel, PriceModel, FileModel
from Baumanagement.models.models_company import Company
from Baumanagement.models.models_currency import Currency
from Baumanagement.models.models_products import Product
from Baumanagement.models.models_projects import Project


@with_author
class ContractTag(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    parent = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True,
                               verbose_name=_('Classify label under'), related_name='children')

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return f'{self.parent}/{self.name}' if self.parent else self.name

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @property
    def count(self):
        return self.contracts.count()

    urls = 'contracttags'
    url_id = 'contracttag_id'
    table_fields = 'name',
    search_fields = 'name',
    form_fields = 'name', 'parent'


@with_author
class Contract(BaseModel, PriceModel, FileModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Contract name'))
    date = models.DateField(null=True, blank=True, verbose_name=_('Date'))
    project = models.ForeignKey(Project, null=False, blank=False, verbose_name=_('Project'),
                                on_delete=models.RESTRICT, related_name='contracts')
    currency = models.ForeignKey(Currency, null=False, blank=False, verbose_name=_('Currency'),
                                 on_delete=models.RESTRICT, related_name='contracts', default=Currency.get_EUR_id)
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='contracts')
    tag = models.ForeignKey(ContractTag, blank=False, verbose_name=_('Tag'),
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
        from Baumanagement.models.models_bills import Bill
        from Baumanagement.models.models_payments import Payment
        bills = Bill.objects.filter(contract_id=OuterRef('pk'), open=True).values(
            'contract__pk').annotate(sum=Sum('amount_brutto_positiv')).values('sum')
        payments = Payment.objects.filter(contract_id=OuterRef('pk'), open=True).values(
            'contract__pk').annotate(sum=Sum('amount_brutto_positiv')).values('sum')
        return qs.annotate(
            bills_amount=Subquery(bills, output_field=DecimalField()) * Case(When(type=PriceModel.BUY, then=-1),
                                                                             default=1),
            payments_amount=Subquery(payments, output_field=DecimalField()) * Case(When(type=PriceModel.BUY, then=-1),
                                                                                   default=1))

    urls = 'contracts'
    url_id = 'contract_id'
    table_fields = 'created', 'project', 'company', 'name', 'date', 'tag', 'files', 'type', 'amount_netto', 'vat', 'amount_brutto', 'bills_amount', 'payments_amount'
    search_fields = 'project__name', 'company__name', 'type', 'name', 'tag__name', 'amount_netto', 'vat', 'amount_brutto', 'bills_amount', 'payments_amount'
    form_fields = 'open', 'project', 'company', 'type', 'name', 'date', 'tag', 'currency', 'amount_netto_positiv', 'vat'


class ContractProduct(PriceModel):
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name=_('Contract'),
                                 on_delete=models.RESTRICT, related_name='products')
    product = models.ForeignKey(Product, null=False, blank=False, verbose_name=_('Product'),
                                 on_delete=models.RESTRICT)
    count = models.FloatField(null=False, blank=False, verbose_name=_('Count'), default=1.0)
    use_product_price = models.BooleanField(default=True)

