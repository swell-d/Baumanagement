from django import forms
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Bill, Contract, Project
from Baumanagement.models.models_company import Company
from Baumanagement.tables.tables_bills import BillTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table

baseClass = Bill
tableClass = BillTable


class FormClass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract'].queryset = Contract.objects.filter(open=True)

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
    return myrender(request, context)


def company_bills(request, id):
    company = Company.objects.get(id=id)
    context = {'titel1': f'{_("Company")} "{company.name}" - {_("Bills")}'}
    queryset = baseClass.objects.filter(contract__company=company)

    form = FormClass()
    form.fields["contract"].queryset = Contract.objects.filter(company=company, open=True)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def project_bills(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Project")} "{project.name}" - {_("Bills")}'}
    queryset = baseClass.objects.filter(contract__project=project)

    form = FormClass()
    form.fields["contract"].queryset = Contract.objects.filter(project=project, open=True)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def contract_bills(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'{_("Contract")} "{contract.name}" - {_("Bills")}'}
    queryset = baseClass.objects.filter(contract=contract)

    form = FormClass()
    form.fields["contract"].initial = contract
    form.fields['contract'].queryset = Contract.objects.filter(id=id)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_bills_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
