from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Project
from Baumanagement.tables import ProjectTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table
from Baumanagement.views.views_contracts import generate_contracts_by_project

baseClass = Project
tableClass = ProjectTable


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {'titel1': _('All projects')}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    queryset = baseClass.objects.filter(id=id)
    context = {'titel1': f'{_("Project")} - {queryset.first().name}', 'tables': []}
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    generate_contracts_by_project(request, context, id)
    return myrender(request, context)
