from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.abstract import add_search_field
from Baumanagement.models.models import Payment, Contract, Project
from Baumanagement.tables import PaymentTable
from Baumanagement.views.views import myrender, new_object_form, edit_object_form

baseClass = Payment


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def payments(request):
    context = {'titel1': _('All payments')}
    new_object_form(request, context, FormClass)

    queryset = baseClass.extra_fields(baseClass.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = PaymentTable(queryset, order_by="id", orderable=request.GET.get('search') is None)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def contract_payments(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'{_("Payments")} - {_("Contract")} - {contract.name}'}
    new_object_form(request, context, FormClass)

    queryset = baseClass.objects.filter(contract=contract)
    queryset = baseClass.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def project_payments(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Payments")} - {_("Project")} - {project.name}'}
    new_object_form(request, context, FormClass)

    queryset = baseClass.objects.filter(contract__in=project.contracts.all())
    queryset = baseClass.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def payment(request, id):
    payment = baseClass.objects.get(id=id)
    context = {'titel1': f'{_("Payment")} - {payment.name}', 'tables': []}
    edit_object_form(request, context, FormClass, payment)

    queryset = baseClass.objects.filter(id=id)
    queryset = baseClass.extra_fields(queryset)
    table1 = PaymentTable(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)
