from django.db.models import Q
from django.shortcuts import render
from django_tables2 import RequestConfig

from Baumanagement.models import Contract, Payment, Bill
from Baumanagement.tables import ContractTable, PaymentTable, BillTable


def contracts(request):
    search = request.GET.get('search')
    queryset = Contract.objects.all()
    if search is not None:
        text_fields = 'project__name', 'company__name', 'name', 'amount_netto', 'vat', 'amount_brutto'
        qs = Q()
        for query in [Q(**{f'{field}__icontains': search}) for field in text_fields]:
            qs = qs | query
        queryset = queryset.filter(qs)

    table1 = ContractTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)

    context = {'titel1': 'Alle Aufträge', 'table1': table1, 'search_field': True, 'url': request.path}
    return render(request,
                  'Baumanagement/maintable.html' if search is not None else 'Baumanagement/tables.html',
                  context)


def contract(request, id):
    tables = []
    contract = Contract.objects.get(id=id)

    table1 = ContractTable(Contract.objects.filter(id=id))
    RequestConfig(request).configure(table1)

    bills = contract.bills.all()
    table = BillTable(bills, order_by="id")
    RequestConfig(request).configure(table)
    tables.append({'table': table, 'titel': 'Rechnungen'})

    payments = contract.payments.all()
    table = PaymentTable(payments, order_by="id")
    RequestConfig(request).configure(table)
    tables.append({'table': table, 'titel': 'Zahlungen'})

    context = {'titel1': f'Auftrag - {contract.name}', 'table1': table1,
               'tables': tables}
    return render(request, 'Baumanagement/tables.html', context)


def contract_bills(request, id):
    contract = Contract.objects.get(id=id)
    table1 = BillTable(Bill.objects.filter(contract=contract), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Rechnungen - Auftrag - {contract.name}', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def contract_payments(request, id):
    contract = Contract.objects.get(id=id)
    table1 = PaymentTable(Payment.objects.filter(contract=contract), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Zahlungen - Auftrag - {contract.name}', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)
