from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Bill, Contract, Project
from Baumanagement.tables import BillTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table

baseClass = Bill
tableClass = BillTable


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {'titel1': _('All bills')}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    queryset = baseClass.objects.filter(id=id)
    context = {'titel1': f'{_("Bill")} - {queryset.first().name}', 'tables': []}
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def contract_bills(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'{_("Bills")} - {_("Contract")} - {contract.name}'}
    queryset = baseClass.objects.filter(contract=contract)
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def project_bills(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Bills")} - {_("Project")} - {project.name}'}
    queryset = baseClass.objects.filter(contract__in=project.contracts.all())
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)
