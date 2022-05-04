from author.decorators import with_author
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel


@with_author
class Currency(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'), unique=True)
    code = models.CharField(max_length=3, null=False, blank=False, verbose_name=_('Code'), unique=True)
    symbol = models.CharField(max_length=3, null=False, blank=False, verbose_name=_('Symbol'), unique=True)
    rate = models.FloatField(verbose_name=_('Rate'), default=1)

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    urls = 'currencies'
    url_id = 'currency_id'
    table_fields = 'name', 'code', 'symbol', 'rate'
    search_fields = 'name', 'code', 'symbol', 'rate'
    form_fields = 'open', 'name', 'code', 'symbol', 'rate'

    @classmethod
    def get_EUR_id(cls):
        eur = cls.objects.filter(name='Euro')
        if eur:
            return eur.first().id
        with transaction.atomic():
            eur = cls.objects.create(name='Euro', code='EUR', symbol='€', rate=1)
        return eur.id
