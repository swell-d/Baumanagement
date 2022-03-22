from django.db.models import Q
from django.shortcuts import render
from django_tables2 import RequestConfig

from Baumanagement.models import Payment
from Baumanagement.tables import PaymentTable


def payments(request):
    search = request.GET.get('search')
    if search is not None:
        text_fields = 'contract__project__name', 'contract__company__name', 'contract__name', \
                      'name', 'amount_netto', 'vat', 'amount_brutto'
        queries = [Q(**{f'{field}__icontains': search}) for field in text_fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        table1 = PaymentTable(Payment.objects.filter(qs), order_by="id")
    else:
        table1 = PaymentTable(Payment.objects.all(), order_by="id")

    RequestConfig(request).configure(table1)

    context = {'titel1': 'Alle Zahlungen', 'table1': table1, 'search': search, 'url': request.path}
    return render(request,
                  'Baumanagement/maintable.html' if search is not None else 'Baumanagement/tables.html',
                  context)


def payment(request, id):
    payment = Payment.objects.get(id=id)

    table1 = PaymentTable(Payment.objects.filter(id=id))
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Zahlung - {payment.name}', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)
