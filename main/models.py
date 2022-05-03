from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    open = models.BooleanField(default=True, null=False, blank=False, verbose_name=_('Open'))
    comment_ids = models.JSONField(default=list, null=False, blank=True, verbose_name=_('Comments'))

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @classmethod
    def verbose_name(cls):
        return cls._meta.verbose_name


class AddressModel(models.Model):
    address = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Address'))
    city = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('City'))
    land = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Land'), default='Deutschland')

    class Meta:
        abstract = True


class PriceModel(models.Model):
    amount_netto_positiv = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,
                                               verbose_name=_('Amount netto'), default=0,
                                               validators=[MinValueValidator(Decimal('0.00'))])
    amount_brutto_positiv = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,
                                                verbose_name=_('Amount brutto'), default=0,
                                                validators=[MinValueValidator(Decimal('0.00'))])
    vat = models.FloatField(null=False, blank=False, verbose_name=_('VAT %'), default=19,
                            validators=[MinValueValidator(float(0))])

    BUY = 'buy'
    SELL = 'sell'
    TYPE_CHOISES = [
        (BUY, _('Buy')),
        (SELL, _('Sell')),
    ]

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.amount_brutto_positiv = Decimal(float(self.amount_netto_positiv) * (1 + self.vat / 100))
        super().save(*args, **kwargs)


class FileModel(models.Model):
    file_ids = models.JSONField(default=list, null=False, blank=True, verbose_name=_('Files'))

    class Meta:
        abstract = True

    @property
    def files(self):
        from Baumanagement.models.models_files import File
        return list(filter(None, [get_or_none(File, id=id) for id in self.file_ids]))


def add_search_field(queryset, request):
    search = request.GET.get('search')
    if search is not None and queryset:
        qs = Q()
        for query in [Q(**{f'{field}__icontains': search}) for field in queryset[0].__class__.search_fields]:
            qs = qs | query
        queryset = queryset.filter(qs)
    return queryset


def get_base_models():
    result = {}
    for cls in BaseModel.__subclasses__():
        result[cls.__name__.lower()] = cls
    return result


def get_or_none(cls, **kwargs):
    try:
        return cls.objects.get(**kwargs)
    except cls.DoesNotExist:
        return None
