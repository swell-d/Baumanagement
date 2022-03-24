from django.forms import ModelForm
from django_tables2 import RequestConfig

from Baumanagement.models import Project, Contract, Payment, Bill, filter_queryset
from Baumanagement.tables import ProjectTable, ContractTable, PaymentTable, BillTable
from Baumanagement.views import myrender


def projects(request):
    context = {'titel1': 'Alle Projekte'}

    if request.method == 'POST':
        formset = ProjectForm(request.POST, request.FILES)
        if formset.is_valid():
            Project(**formset.cleaned_data).save()
    context['form'] = ProjectForm()
    context['buttons'] = ['Neu']

    queryset = Project.extra_fields(Project.objects)
    queryset = filter_queryset(queryset, request)
    context['search_field'] = True
    table1 = ProjectTable(queryset, order_by="name")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def project(request, id):
    tables = []
    project = Project.objects.get(id=id)

    if request.method == 'POST':
        formset = ProjectForm(request.POST, request.FILES, instance=project)
        if formset.is_valid():
            project.save()

    queryset = Project.objects.filter(id=id)
    queryset = Project.extra_fields(queryset)
    table1 = ProjectTable(queryset)
    RequestConfig(request).configure(table1)

    contracts = Contract.objects.filter(project=id)
    contracts = Contract.extra_fields(contracts)
    if contracts:
        table = ContractTable(contracts, order_by="name")
        RequestConfig(request).configure(table)
        tables.append({'table': table, 'titel': 'Aufträge'})

    form = ProjectForm(instance=project)
    context = {'titel1': f'Projekt - {project.name}', 'table1': table1,
               'tables': tables, 'form': form}
    return myrender(request, context)


def project_payments(request, id):
    project = Project.objects.get(id=id)
    queryset = Payment.objects.filter(contract__in=project.contracts.all())
    queryset = Payment.extra_fields(queryset)
    queryset = filter_queryset(queryset, request)
    table1 = PaymentTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Zahlungen - Projekt - {project.name}', 'table1': table1, 'search_field': True}
    return myrender(request, context)


def project_bills(request, id):
    project = Project.objects.get(id=id)
    queryset = Bill.objects.filter(contract__in=project.contracts.all())
    queryset = Bill.extra_fields(queryset)
    queryset = filter_queryset(queryset, request)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Rechnungen - Projekt - {project.name}', 'table1': table1, 'search_field': True}
    return myrender(request, context)


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = Project.form_fields()
