from django.shortcuts import render
from django_tables2 import RequestConfig

from Baumanagement.models import Bill
from Baumanagement.tables import BillTable


def bills(request):
    table1 = BillTable(Bill.objects.all(), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Rechnungen', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def bill(request, id):
    bill = Bill.objects.get(id=id)

    table1 = BillTable(Bill.objects.filter(id=id))
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Rechnung - {bill.name}', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)
