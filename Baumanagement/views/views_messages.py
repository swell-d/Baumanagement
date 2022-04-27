from django import forms
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_messages import MyMessage
from Baumanagement.tables.tables import MyTable
from Baumanagement.views.views import myrender, generate_objects_table, get_base_context, generate_object_table

baseClass = MyMessage


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


def objects_table(request):
    context = get_base_context(request)
    queryset = MyMessage.objects.filter(author=request.user)
    generate_objects_table(request, context, baseClass, TableClass, FormClass, queryset)
    return myrender(request, context)


def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': queryset.first().id}]

    generate_object_table(request, context, baseClass, TableClass, FormClass, queryset)
    return myrender(request, context)
