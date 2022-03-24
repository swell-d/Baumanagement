from django.forms import ModelForm
from django_tables2 import RequestConfig

from Baumanagement.models import Payment, filter_queryset, Contract
from Baumanagement.tables import PaymentTable
from Baumanagement.views import myrender


def payments(request):
    context = {'titel1': 'Alle Zahlungen'}

    if request.method == 'POST':
        formset = PaymentForm(request.POST, request.FILES)
        if formset.is_valid():
            Payment(**formset.cleaned_data).save()
    context['form'] = PaymentForm()
    context['buttons'] = ['New']

    queryset = Payment.extra_fields(Payment.objects)
    queryset = filter_queryset(queryset, request)
    context['search_field'] = True
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def contract_payments(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'Zahlungen - Auftrag - {contract.name}'}

    if request.method == 'POST':
        formset = PaymentForm(request.POST, request.FILES)
        if formset.is_valid():
            Payment(**formset.cleaned_data).save()
    context['form'] = PaymentForm()
    context['buttons'] = ['New']

    queryset = Payment.objects.filter(contract=contract)
    queryset = Payment.extra_fields(queryset)
    context['search_field'] = True
    queryset = filter_queryset(queryset, request)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def payment(request, id):
    payment = Payment.objects.get(id=id)
    context = {'titel1': f'Zahlung - {payment.name}', 'tables': []}

    if request.method == 'POST':
        formset = PaymentForm(request.POST, request.FILES, instance=payment)
        if formset.is_valid():
            payment.save()
    context['form'] = PaymentForm(instance=payment)
    context['buttons'] = ['Edit']

    queryset = Payment.objects.filter(id=id)
    queryset = Payment.extra_fields(queryset)
    table1 = PaymentTable(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = Payment.form_fields()
