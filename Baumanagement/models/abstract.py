from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


def add_search_field(queryset, request, context):
    search = request.GET.get('search')
    if search is not None and queryset:
        qs = Q()
        for query in [Q(**{f'{field}__icontains': search}) for field in queryset[0].__class__.search_fields]:
            qs = qs | query
        queryset = queryset.filter(qs)
    context['search_field'] = True
    return queryset


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    open = models.BooleanField(default=True, null=False, blank=False, verbose_name=_('Open'))
    comment_ids = models.JSONField(default=list, null=False, blank=True, verbose_name=_('Comments'))
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if kwargs.get('user'):
            self.created_by = kwargs.pop('user')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AddressModel(models.Model):
    address = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Address'))
    city = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('City'))
    land = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Land'), default='Deutschland')

    class Meta:
        abstract = True


class PriceModel(models.Model):
    amount_netto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,
                                       verbose_name=_('Amount netto'))
    vat = models.FloatField(null=False, blank=False, verbose_name=_('VAT %'), default=19)
    amount_brutto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,
                                        verbose_name=_('Amount brutto'))

    class Meta:
        abstract = True


class FileModel(models.Model):
    file_ids = models.JSONField(default=list, null=False, blank=True, verbose_name=_('Files'))

    class Meta:
        abstract = True

    @property
    def files(self):
        from Baumanagement.models.models_files import File
        return [File.objects.get(id=id) for id in self.file_ids]
