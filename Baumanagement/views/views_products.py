from django import forms
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_products import Product
from Baumanagement.tables.tables_products import ProductTable
from Baumanagement.views.views import myrender, generate_object_table, generate_objects_table, get_base_context

baseClass = Product
tableClass = ProductTable


class FormClass(forms.ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = get_base_context(request)
    context['tags1'] = tags()
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': queryset.first()}]

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def tags():
    html = '&#9881;<a href="' + reverse('productcategories') + '">' + _('Manage categories') + '</a>'
    return format_html(html)
