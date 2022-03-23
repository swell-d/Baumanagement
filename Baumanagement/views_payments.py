from django.forms import ModelForm
from django_tables2 import RequestConfig

from Baumanagement.models import Payment, filter_queryset
from Baumanagement.tables import PaymentTable
from Baumanagement.views import myrender


def payments(request):
    queryset = Payment.objects
    queryset = Payment.extra_fields(queryset)
    queryset = filter_queryset(queryset, request)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Zahlungen', 'table1': table1, 'search_field': True}
    return myrender(request, context)


def payment(request, id):
    payment = Payment.objects.get(id=id)

    if request.method == 'POST':
        formset = PaymentForm(request.POST, request.FILES, instance=payment)
        if formset.is_valid():
            payment.save()

    queryset = Payment.objects.filter(id=id)
    queryset = Payment.extra_fields(queryset)
    table1 = PaymentTable(queryset)
    RequestConfig(request).configure(table1)

    form = PaymentForm(instance=payment)
    context = {'titel1': f'Zahlung - {payment.name}', 'table1': table1, 'form': form}
    return myrender(request, context)


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = Payment.form_fields()
