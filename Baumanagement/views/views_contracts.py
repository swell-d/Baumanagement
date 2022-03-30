from django.contrib import messages
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Contract
from Baumanagement.tables import ContractTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table
from Baumanagement.views.views_bills import generate_bills_by_contract
from Baumanagement.views.views_payments import generate_payments_by_contract

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
    queryset = baseClass.objects.filter(id=id)
    context = {'titel1': f'{_("Contract")} - {queryset.first().name}', 'tables': []}
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)

    disable_children(request, queryset.first())

    bills = queryset.first().bills.all()
    generate_bills_by_contract(request, context, bills)

    payments = queryset.first().payments.all()
    generate_payments_by_contract(request, context, payments)

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


def generate_contracts_by_project(request, context, id):
    queryset = baseClass.objects.filter(project=id)
    generate_next_objects_table(request, context, baseClass, tableClass, FormClass, queryset, _("Contracts"))
