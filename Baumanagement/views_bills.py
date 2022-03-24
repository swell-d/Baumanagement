from django.forms import ModelForm
from django_tables2 import RequestConfig

from Baumanagement.models import Bill, add_search_field, Contract, Project
from Baumanagement.tables import BillTable
from Baumanagement.views import myrender


def bills(request):
    context = {'titel1': 'Alle Rechnungen'}
    form_new_bill(request, context)

    queryset = Bill.extra_fields(Bill.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def contract_bills(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'Rechnungen - Auftrag - {contract.name}'}
    form_new_bill(request, context)

    queryset = Bill.objects.filter(contract=contract)
    queryset = Bill.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def project_bills(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'Rechnungen - Projekt - {project.name}'}
    form_new_bill(request, context)

    queryset = Bill.objects.filter(contract__in=project.contracts.all())
    queryset = Bill.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def bill(request, id):
    bill = Bill.objects.get(id=id)
    context = {'titel1': f'Rechnung - {bill.name}', 'tables': []}
    form_edit_bill(request, context, bill)

    queryset = Bill.objects.filter(id=id)
    queryset = Bill.extra_fields(queryset)
    table1 = BillTable(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = Bill.form_fields()


def form_new_bill(request, context):
    if request.method == 'POST':
        formset = BillForm(request.POST, request.FILES)
        if formset.is_valid():
            Bill(**formset.cleaned_data).save()
    context['form'] = BillForm()
    context['buttons'] = ['New']


def form_edit_bill(request, context, bill):
    if request.method == 'POST':
        formset = BillForm(request.POST, request.FILES, instance=bill)
        if formset.is_valid():
            bill.save()
    context['form'] = BillForm(instance=bill)
    context['buttons'] = ['Edit']
