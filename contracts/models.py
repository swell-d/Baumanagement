from author.decorators import with_author
from django.db import models
from django.db.models import OuterRef, Sum, Subquery, DecimalField, Case, When
from django.utils.translation import gettext_lazy as _

from companies.models import Company
from contracts.models_labels import ContractLabel
from currencies.models import Currency
from main.models import BaseModel, PriceModel, FileModel
from projects.models import Project


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
    label = models.ManyToManyField(ContractLabel, blank=True, verbose_name=_('Labels'), related_name='contracts')

    BUY = PriceModel.BUY
    SELL = PriceModel.SELL
    TYPE_CHOISES = PriceModel.TYPE_CHOISES
    type = models.CharField(max_length=4, choices=TYPE_CHOISES,
                            default=PriceModel.BUY, verbose_name=_('Contract type'))

    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.products.all():
            from products.models import Product
            base_service = Product.objects.get_or_create(name=_('Base service'), type=Product.SERVICE)[0]
            from contracts.models_products import ContractProduct
            ContractProduct.objects.create(contract=self, product=base_service, use_product_price=False,
                                           amount_netto_positiv=self.amount_netto_positiv, vat=self.vat,
                                           amount_brutto_positiv=self.amount_brutto_positiv)

    @staticmethod
    def extra_fields(qs):
        from bills.models import Bill
        from payments.models import Payment
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
    table_fields = 'created', 'project', 'company', 'name', 'date', 'label', 'files', 'type', 'amount_netto', 'amount_brutto', 'bills_amount', 'payments_amount'
    search_fields = 'project__name', 'company__name', 'name', 'type', 'amount_netto', 'amount_brutto', 'bills_amount', 'payments_amount'
    form_fields = 'open', 'project', 'company', 'type', 'name', 'date', 'label', 'currency'
