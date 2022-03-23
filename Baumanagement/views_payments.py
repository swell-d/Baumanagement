from django_tables2 import RequestConfig

from Baumanagement.models import Payment, filter_queryset
from Baumanagement.tables import PaymentTable
from Baumanagement.views import myrender


def payments(request):
    queryset = Payment.objects.all()
    queryset = filter_queryset(queryset, request)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Zahlungen', 'table1': table1, 'search_field': True}
    return myrender(request, context)


def payment(request, id):
    payment = Payment.objects.get(id=id)

    table1 = PaymentTable(Payment.objects.filter(id=id))
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Zahlung - {payment.name}', 'table1': table1}
    return myrender(request, context)
