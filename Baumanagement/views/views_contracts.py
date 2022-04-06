from django import forms
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Contract, Project
from Baumanagement.models.models_company import Company
from Baumanagement.tables.tables_contracts import ContractTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table
from Baumanagement.views.views_bills import generate_bills_by_queryset
from Baumanagement.views.views_payments import generate_payments_by_queryset

baseClass = Contract
tableClass = ContractTable


class FormClass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(open=True)
        self.fields['company'].queryset = Company.objects.filter(open=True)

    class Meta:
        model = baseClass
        fields = baseClass.form_fields
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}


def objects_table(request):
    context = {}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    context = {'tables': []}
    queryset = baseClass.objects.filter(id=id)
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)

    disable_children(request, queryset.first())

    bills = queryset.first().bills.all()
    generate_bills_by_queryset(request, context, bills)

    payments = queryset.first().payments.all()
    generate_payments_by_queryset(request, context, payments)

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


def company_contracts(request, id):
    company = Company.objects.get(id=id)
    context = {'titel1': f'{_("Company")} "{company.name}" - {_("Contracts")}'}
    queryset = baseClass.objects.filter(Q(project__company=company) | Q(company=company))
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def project_contracts(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Project")} "{project.name}" - {_("Contracts")}'}
    queryset = project.contracts.all()

    form = FormClass()
    form.fields["project"].initial = project
    form.fields['project'].queryset = Project.objects.filter(id=id)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_contracts_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
