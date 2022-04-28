import django_tables2 as tables
from django import forms
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_comments import Comment
from Baumanagement.tables.tables import MyTable, Files
from Baumanagement.views.views import myrender, generate_object_table, generate_objects_table, get_base_context

baseClass = Comment


class TableClass(MyTable, Files):
    class Meta(MyTable.Meta):
        model = baseClass
        fields = baseClass.table_fields

    files = tables.Column(verbose_name=_('Files'), orderable=False)


class FormClass(forms.ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = get_base_context(request)
    generate_objects_table(request, context, baseClass, TableClass, FormClass)
    if request.method == 'POST' and request.POST.get('newCommentNextURL'):
        return redirect(request.POST.get('newCommentNextURL'))
    return myrender(request, context)


def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    if queryset.first() is None:
        raise Http404

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': queryset.first().id}]

    generate_object_table(request, context, baseClass, TableClass, FormClass, queryset)
    return myrender(request, context)
