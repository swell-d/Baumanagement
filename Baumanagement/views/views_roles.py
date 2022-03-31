from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import CompanyRole
from Baumanagement.tables.tables_roles import CompanyRoleTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table

baseClass = CompanyRole
tableClass = CompanyRoleTable


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {'titel1': _('All roles')}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    queryset = baseClass.objects.filter(id=id)
    context = {'titel1': f'{_("Role")} - {queryset.first().name}', 'tables': []}
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)
