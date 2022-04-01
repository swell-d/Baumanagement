from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Contact
from Baumanagement.tables.tables_contacts import ContactTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table

baseClass = Contact
tableClass = ContactTable


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    queryset = baseClass.objects.filter(id=id)
    context = {'titel1': f'{_("Contact")} - {queryset.first().name}', 'tables': []}
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_contacts_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
