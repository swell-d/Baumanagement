from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Payment, Contract, Project
from Baumanagement.models.models_company import Company
from Baumanagement.tables.tables_payments import PaymentTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table

baseClass = Payment
tableClass = PaymentTable


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    context = {'tables': []}
    queryset = baseClass.objects.filter(id=id)
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def company_payments(request, id):
    company = Company.objects.get(id=id)
    context = {'titel1': f'{_("Company")} "{company.name}" - {_("Payments")}'}
    queryset = baseClass.objects.filter(contract__company=company)
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def project_payments(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Project")} "{project.name}" - {_("Payments")}'}
    queryset = baseClass.objects.filter(contract__project=project)
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def contract_payments(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'{_("Contract")} "{contract.name}" - {_("Payments")}'}
    queryset = baseClass.objects.filter(contract=contract)
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_payments_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
