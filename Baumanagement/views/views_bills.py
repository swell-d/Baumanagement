from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.abstract import add_search_field
from Baumanagement.models.models import Bill, Contract, Project
from Baumanagement.tables import BillTable
from Baumanagement.views.views import myrender, new_object_form, edit_object_form

baseClass = Bill


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def bills(request):
    context = {'titel1': _('All bills')}
    new_object_form(request, context, FormClass)

    queryset = baseClass.extra_fields(baseClass.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id", orderable=request.GET.get('search') is None)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def contract_bills(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'{_("Bills")} - {_("Contract")} - {contract.name}'}
    new_object_form(request, context, FormClass)

    queryset = baseClass.objects.filter(contract=contract)
    queryset = baseClass.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def project_bills(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Bills")} - {_("Project")} - {project.name}'}
    new_object_form(request, context, FormClass)

    queryset = baseClass.objects.filter(contract__in=project.contracts.all())
    queryset = baseClass.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def bill(request, id):
    bill = baseClass.objects.get(id=id)
    context = {'titel1': f'{_("Bill")} - {bill.name}', 'tables': []}
    edit_object_form(request, context, FormClass, bill)

    queryset = baseClass.objects.filter(id=id)
    queryset = baseClass.extra_fields(queryset)
    table1 = BillTable(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)
