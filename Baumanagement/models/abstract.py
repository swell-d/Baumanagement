from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


def add_search_field(queryset, request, context):
    search = request.GET.get('search')
    if search is not None:
        qs = Q()
        for query in [Q(**{f'{field}__icontains': search}) for field in queryset[0].__class__.search_fields()]:
            qs = qs | query
        queryset = queryset.filter(qs)
    context['search_field'] = True
    return queryset


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    open = models.BooleanField(default=True, null=False, blank=False, verbose_name=_('Open'))

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AddressModel(models.Model):
    address = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Address'))
    city = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('City'))
    land = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Land'), default='Deutschland')

    class Meta:
        abstract = True
