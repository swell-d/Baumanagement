from django.shortcuts import render
from django_tables2 import RequestConfig

from Baumanagement.filters import PaymentFilter, filter_form_prettify
from Baumanagement.models import Payment
from Baumanagement.tables import PaymentTable


def payments(request):
    filter = PaymentFilter(request.GET, queryset=Payment.objects.all())
    table1 = PaymentTable(filter.qs, order_by="id")
    RequestConfig(request).configure(table1)
    filter_form = filter_form_prettify(filter.form)

    context = {'titel1': 'Alle Zahlungen', 'table1': table1,
               'filter': filter, 'filter_form': filter_form}
    return render(request, 'Baumanagement/tables.html', context)


def payment(request, id):
    payment = Payment.objects.get(id=id)

    table1 = PaymentTable(Payment.objects.filter(id=id))
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Zahlung - {payment.name}', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)
