from django.contrib import messages
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.models import Contract, Payment, Bill
from Baumanagement.tables import ContractTable, PaymentTable, BillTable
from Baumanagement.views.views import myrender, edit_object_form, generate_objects_table

baseClass = Contract
tableClass = ContractTable


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {'titel1': _("All contracts")}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    contract = baseClass.objects.get(id=id)
    context = {'titel1': f'{_("Contract")} - {contract.name}', 'tables': []}
    edit_object_form(request, context, FormClass, contract)
    disable_children(request, contract)

    queryset = baseClass.objects.filter(id=id)
    queryset = baseClass.extra_fields(queryset)
    table1 = tableClass(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    bills = contract.bills.all()
    bills = Bill.extra_fields(bills)
    table = BillTable(bills, order_by="id")
    RequestConfig(request).configure(table)
    context['tables'].append({'table': table, 'titel': _("Bills")})

    payments = contract.payments.all()
    payments = Payment.extra_fields(payments)
    table = PaymentTable(payments, order_by="id")
    RequestConfig(request).configure(table)
    context['tables'].append({'table': table, 'titel': _("Payments")})

    return myrender(request, context)


def disable_children(request, contract):
    if request.method == 'POST' and not contract.open:
        for bill in contract.bills.all():
            if bill.open:
                bill.open = False
                messages.warning(request, f'{bill.name} {_("disabled")}')
                bill.save()
        for payment in contract.payments.all():
            if payment.open:
                payment.open = False
                messages.warning(request, f'{payment.name} {_("disabled")}')
                payment.save()
