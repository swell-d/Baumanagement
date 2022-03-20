from django.shortcuts import render
from django_tables2 import RequestConfig

from Baumanagement.models import Contract, Payment, Bill
from Baumanagement.tables import ContractTable, PaymentTable, BillTable


def contracts(request):
    table1 = ContractTable(Contract.objects.all(), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Aufträge', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def contract(request, id):
    contract = Contract.objects.get(id=id)

    table1 = ContractTable(Contract.objects.filter(id=id))
    RequestConfig(request).configure(table1)

    bills = contract.bills.all()
    table4 = BillTable(bills, order_by="id")
    RequestConfig(request).configure(table4)

    payments = contract.payments.all()
    table5 = PaymentTable(payments, order_by="id")
    RequestConfig(request).configure(table5)

    context = {'titel1': f'Auftrag - {contract.name}', 'table1': table1,
               'titel4': 'Rechnungen', 'table4': table4,
               'titel5': 'Zahlungen', 'table5': table5}
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
