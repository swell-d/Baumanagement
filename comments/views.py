import django_tables2 as tables
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from comments.models import Comment
from main.tables import MyTable, Files
from main.views import get_base_context, generate_objects_table, myrender, generate_object_table

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


@login_required
def objects_table(request):
    context = get_base_context(request)
    generate_objects_table(request, context, baseClass, TableClass, FormClass)
    if request.method == 'POST' and request.POST.get('newCommentNextURL'):
        return redirect(request.POST.get('newCommentNextURL'))
    return myrender(request, context)


@login_required
def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    if queryset.first() is None:
        raise Http404

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': queryset.first().id}]

    generate_object_table(request, context, baseClass, TableClass, FormClass, queryset)
    return myrender(request, context)
