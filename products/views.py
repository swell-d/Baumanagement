from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from main.view_renders import myrender
from main.views import get_base_context, generate_objects_table, generate_object_table
from products.models import Product
from products.models_labels import ProductCategory
from products.tables import ProductTable

baseClass = Product
tableClass = ProductTable
labelClass = ProductCategory


class FormClass(forms.ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


@login_required
def objects_table(request):
    context = get_base_context(request)
    context['categories'] = {'objects': labelClass.objects.order_by('path'),
                             'urls': labelClass.urls}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


@login_required
def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    if queryset.first() is None:
        raise Http404

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': queryset.first()}]

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)
