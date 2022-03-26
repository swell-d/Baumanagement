from django.contrib import messages
from django.forms import ModelForm
from django_tables2 import RequestConfig

from Baumanagement.models import Payment, add_search_field, Contract, Project
from Baumanagement.tables import PaymentTable
from Baumanagement.views import myrender, upload_files


def payments(request):
    context = {'titel1': 'Alle Zahlungen'}
    form_new_payment(request, context)

    queryset = Payment.extra_fields(Payment.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def contract_payments(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'Zahlungen - Auftrag - {contract.name}'}
    form_new_payment(request, context)

    queryset = Payment.objects.filter(contract=contract)
    queryset = Payment.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def project_payments(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'Zahlungen - Projekt - {project.name}'}
    form_new_payment(request, context)

    queryset = Payment.objects.filter(contract__in=project.contracts.all())
    queryset = Payment.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def payment(request, id):
    payment = Payment.objects.get(id=id)
    context = {'titel1': f'Zahlung - {payment.name}', 'tables': []}
    form_edit_payment(request, context, payment)

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


def form_new_payment(request, context):
    if request.method == 'POST':
        formset = PaymentForm(request.POST, request.FILES)
        if formset.is_valid():
            new_object = Payment(**formset.cleaned_data)
            new_object.save()
            messages.success(request, f'{new_object.name} hinzugefügt')
            upload_files(request, payment=new_object)
    context['form'] = PaymentForm()
    context['files_form'] = []
    context['buttons'] = ['New']


def form_edit_payment(request, context, payment):
    if request.method == 'POST':
        formset = PaymentForm(request.POST, request.FILES, instance=payment)
        if formset.is_valid():
            payment.save()
            messages.success(request, f'{payment.name} geändert')
            upload_files(request, payment=payment)
    context['form'] = PaymentForm(instance=payment)
    context['files_form'] = payment.files.all()
    context['buttons'] = ['Edit']


