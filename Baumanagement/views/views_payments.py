from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.abstract import add_search_field
from Baumanagement.models.models import Payment, Contract, Project
from Baumanagement.tables import PaymentTable
from Baumanagement.views.views import myrender, new_object_form, edit_object_form


def payments(request):
    context = {'titel1': _('All payments')}
    new_object_form(request, context, PaymentForm)

    queryset = Payment.extra_fields(Payment.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = PaymentTable(queryset, order_by="id", orderable=request.GET.get('search') is None)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def contract_payments(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'{_("Payments")} - {_("Contract")} - {contract.name}'}
    new_object_form(request, context, PaymentForm)

    queryset = Payment.objects.filter(contract=contract)
    queryset = Payment.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def project_payments(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Payments")} - {_("Project")} - {project.name}'}
    new_object_form(request, context, PaymentForm)

    queryset = Payment.objects.filter(contract__in=project.contracts.all())
    queryset = Payment.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def payment(request, id):
    payment = Payment.objects.get(id=id)
    context = {'titel1': f'{_("Payment")} - {payment.name}', 'tables': []}
    edit_object_form(request, context, PaymentForm, payment)

    queryset = Payment.objects.filter(id=id)
    queryset = Payment.extra_fields(queryset)
    table1 = PaymentTable(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = Payment.form_fields
