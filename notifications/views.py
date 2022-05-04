from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from main.tables import MyTable
from main.views import get_base_context, generate_objects_table, myrender, generate_object_table
from notifications.models import Notification

baseClass = Notification


class TableClass(MyTable):
    class Meta(MyTable.Meta):
        model = baseClass
        fields = baseClass.table_fields

    def render_name(self, record, value):
        return format_html(value)

    def render_level(self, record, value):
        return format_html(f'<div class="{record.bootstrap_class()}">{record.level_tag()}</div>')


class FormClass(forms.ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


@login_required
def objects_table(request):
    context = get_base_context(request)
    queryset = Notification.objects.filter(author=request.user)
    generate_objects_table(request, context, baseClass, TableClass, FormClass, queryset)
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
