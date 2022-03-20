from django.shortcuts import render
from django_tables2 import RequestConfig

from Baumanagement.models import Payment
from Baumanagement.tables import PaymentTable


def payments(request):
    table1 = PaymentTable(Payment.objects.all(), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Zahlungen', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def payment(request, id):
    payment = Payment.objects.get(id=id)

    table1 = PaymentTable(Payment.objects.filter(id=id))
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Zahlung - {payment.name}', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)
