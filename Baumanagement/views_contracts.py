from django_tables2 import RequestConfig

from Baumanagement.models import Contract, Payment, Bill, filter_queryset
from Baumanagement.tables import ContractTable, PaymentTable, BillTable
from Baumanagement.views import myrender


def contracts(request):
    queryset = Contract.objects
    queryset = Contract.extra_fields(queryset)
    queryset = filter_queryset(queryset, request)
    table1 = ContractTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Aufträge', 'table1': table1, 'search_field': True}
    return myrender(request, context)


def contract(request, id):
    tables = []
    contract = Contract.objects.get(id=id)

    queryset = Contract.objects.filter(id=id)
    queryset = Contract.extra_fields(queryset)
    table1 = ContractTable(queryset)
    RequestConfig(request).configure(table1)

    bills = contract.bills.all()
    bills = Bill.extra_fields(bills)
    table = BillTable(bills, order_by="id")
    RequestConfig(request).configure(table)
    tables.append({'table': table, 'titel': 'Rechnungen'})

    payments = contract.payments.all()
    payments = Payment.extra_fields(payments)
    table = PaymentTable(payments, order_by="id")
    RequestConfig(request).configure(table)
    tables.append({'table': table, 'titel': 'Zahlungen'})

    context = {'titel1': f'Auftrag - {contract.name}', 'table1': table1,
               'tables': tables}
    return myrender(request, context)


def contract_bills(request, id):
    contract = Contract.objects.get(id=id)
    queryset = Bill.objects.filter(contract=contract)
    queryset = filter_queryset(queryset, request)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Rechnungen - Auftrag - {contract.name}', 'table1': table1, 'search_field': True}
    return myrender(request, context)


def contract_payments(request, id):
    contract = Contract.objects.get(id=id)
    queryset = Payment.objects.filter(contract=contract)
    queryset = filter_queryset(queryset, request)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Zahlungen - Auftrag - {contract.name}', 'table1': table1, 'search_field': True}
    return myrender(request, context)
