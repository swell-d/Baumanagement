from django_tables2 import RequestConfig

from Baumanagement.models import Contract, Payment, Bill
from Baumanagement.search_fields import contracts_search_fields, filter_queryset, bills_search_fields, \
    payments_search_fields
from Baumanagement.tables import ContractTable, PaymentTable, BillTable
from Baumanagement.views import myrender


def contracts(request):
    queryset = Contract.objects.all()
    queryset = filter_queryset(queryset, request, contracts_search_fields)
    table1 = ContractTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Aufträge', 'table1': table1, 'search_field': True}
    return myrender(request, context)


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
    return myrender(request, context)


def contract_bills(request, id):
    contract = Contract.objects.get(id=id)
    queryset = Bill.objects.filter(contract=contract)
    queryset = filter_queryset(queryset, request, bills_search_fields)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Rechnungen - Auftrag - {contract.name}', 'table1': table1, 'search_field': True}
    # breakpoint()
    return myrender(request, context)


def contract_payments(request, id):
    contract = Contract.objects.get(id=id)
    queryset = Payment.objects.filter(contract=contract)
    queryset = filter_queryset(queryset, request, payments_search_fields)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Zahlungen - Auftrag - {contract.name}', 'table1': table1, 'search_field': True}
    return myrender(request, context)
