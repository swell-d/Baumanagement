from django.forms import ModelForm
from django_tables2 import RequestConfig

from Baumanagement.models import Contract, Payment, Bill, add_search_field
from Baumanagement.tables import ContractTable, PaymentTable, BillTable
from Baumanagement.views import myrender


def contracts(request):
    context = {'titel1': 'Alle Aufträge'}

    if request.method == 'POST':
        formset = ContractForm(request.POST, request.FILES)
        if formset.is_valid():
            Contract(**formset.cleaned_data).save()
    context['form'] = ContractForm()
    context['buttons'] = ['New']

    queryset = Contract.extra_fields(Contract.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = ContractTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def contract(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'Auftrag - {contract.name}', 'tables': []}

    if request.method == 'POST':
        formset = ContractForm(request.POST, request.FILES, instance=contract)
        if formset.is_valid():
            contract.save()
    context['form'] = ContractForm(instance=contract)
    context['buttons'] = ['Edit']

    queryset = Contract.objects.filter(id=id)
    queryset = Contract.extra_fields(queryset)
    table1 = ContractTable(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    bills = contract.bills.all()
    bills = Bill.extra_fields(bills)
    table = BillTable(bills, order_by="id")
    RequestConfig(request).configure(table)
    context['tables'].append({'table': table, 'titel': 'Rechnungen'})

    payments = contract.payments.all()
    payments = Payment.extra_fields(payments)
    table = PaymentTable(payments, order_by="id")
    RequestConfig(request).configure(table)
    context['tables'].append({'table': table, 'titel': 'Zahlungen'})

    return myrender(request, context)


class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = Contract.form_fields()
