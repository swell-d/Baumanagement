from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.models import Project, Contract
from Baumanagement.tables import ProjectTable, ContractTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table

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

    contracts = Contract.objects.filter(project=id)
    contracts = Contract.extra_fields(contracts)
    if contracts:
        table = ContractTable(contracts, order_by="name")
        RequestConfig(request).configure(table)
        context['tables'].append({'table': table, 'titel': _("Contracts")})

    return myrender(request, context)
