from django import forms
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Project, Bill, Payment
from Baumanagement.models.models_company import Company
from Baumanagement.tables.tables_projects import ProjectTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table
from Baumanagement.views.views_bills import generate_bills_by_queryset
from Baumanagement.views.views_contracts import generate_contracts_by_queryset
from Baumanagement.views.views_payments import generate_payments_by_queryset

baseClass = Project
tableClass = ProjectTable


class FormClass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(open=True)

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

    contracts = queryset.first().contracts.all()
    generate_contracts_by_queryset(request, context, contracts)

    bills = Bill.objects.filter(contract__project=queryset.first())
    generate_bills_by_queryset(request, context, bills)

    payments = Payment.objects.filter(contract__project=queryset.first())
    generate_payments_by_queryset(request, context, payments)

    return myrender(request, context)


def company_projects(request, id):
    company = Company.objects.get(id=id)
    context = {'titel1': f'{_("Company")} "{company.name}" - {_("Projects")}'}
    queryset = company.projects.all()

    form = FormClass()
    form.fields["company"].initial = company
    form.fields['company'].queryset = Company.objects.filter(id=id)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_projects_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
