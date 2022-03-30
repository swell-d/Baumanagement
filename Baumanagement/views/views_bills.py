from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.abstract import add_search_field
from Baumanagement.models.models import Bill, Contract, Project
from Baumanagement.tables import BillTable
from Baumanagement.views.views import myrender, new_object_form, edit_object_form


def bills(request):
    context = {'titel1': _('All bills')}
    new_object_form(request, context, BillForm)

    queryset = Bill.extra_fields(Bill.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id", orderable=request.GET.get('search') is None)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def contract_bills(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'{_("Bills")} - {_("Contract")} - {contract.name}'}
    new_object_form(request, context, BillForm)

    queryset = Bill.objects.filter(contract=contract)
    queryset = Bill.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def project_bills(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Bills")} - {_("Project")} - {project.name}'}
    new_object_form(request, context, BillForm)

    queryset = Bill.objects.filter(contract__in=project.contracts.all())
    queryset = Bill.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def bill(request, id):
    bill = Bill.objects.get(id=id)
    context = {'titel1': f'{_("Bill")} - {bill.name}', 'tables': []}
    edit_object_form(request, context, BillForm, bill)

    queryset = Bill.objects.filter(id=id)
    queryset = Bill.extra_fields(queryset)
    table1 = BillTable(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = Bill.form_fields
