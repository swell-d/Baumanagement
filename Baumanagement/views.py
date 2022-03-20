from django.shortcuts import render
from django_tables2 import RequestConfig

from Baumanagement.models import Payment, Bill
from Baumanagement.tables import PaymentTable, BillTable


def payments(request):
    table1 = PaymentTable(Payment.objects.all(), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Zahlungen', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def bills(request):
    table1 = BillTable(Bill.objects.all(), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Rechnungen', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)
