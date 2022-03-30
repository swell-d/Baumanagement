from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.models import Project, Contract
from Baumanagement.tables import ProjectTable, ContractTable
from Baumanagement.views.views import myrender, edit_object_form, generate_objects_table

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
    project = baseClass.objects.get(id=id)
    context = {'titel1': f'{_("Project")} - {project.name}', 'tables': []}
    edit_object_form(request, context, FormClass, project)

    queryset = baseClass.objects.filter(id=id)
    queryset = baseClass.extra_fields(queryset)
    table1 = tableClass(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    contracts = Contract.objects.filter(project=id)
    contracts = Contract.extra_fields(contracts)
    if contracts:
        table = ContractTable(contracts, order_by="name")
        RequestConfig(request).configure(table)
        context['tables'].append({'table': table, 'titel': _("Contracts")})

    return myrender(request, context)
