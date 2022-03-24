from django.forms import ModelForm
from django_tables2 import RequestConfig

from Baumanagement.models import Project, Contract, add_search_field
from Baumanagement.tables import ProjectTable, ContractTable
from Baumanagement.views import myrender


def projects(request):
    context = {'titel1': 'Alle Projekte'}
    form_new_project(request, context)

    queryset = Project.extra_fields(Project.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = ProjectTable(queryset, order_by="name")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def project(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'Projekt - {project.name}', 'tables': []}
    form_edit_project(request, context, project)

    queryset = Project.objects.filter(id=id)
    queryset = Project.extra_fields(queryset)
    table1 = ProjectTable(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    contracts = Contract.objects.filter(project=id)
    contracts = Contract.extra_fields(contracts)
    if contracts:
        table = ContractTable(contracts, order_by="name")
        RequestConfig(request).configure(table)
        context['tables'].append({'table': table, 'titel': 'Aufträge'})

    return myrender(request, context)


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = Project.form_fields()


def form_new_project(request, context):
    if request.method == 'POST':
        formset = ProjectForm(request.POST, request.FILES)
        if formset.is_valid():
            Project(**formset.cleaned_data).save()
    context['form'] = ProjectForm()
    context['buttons'] = ['New']


def form_edit_project(request, context, project):
    if request.method == 'POST':
        formset = ProjectForm(request.POST, request.FILES, instance=project)
        if formset.is_valid():
            project.save()
    context['form'] = ProjectForm(instance=project)
    context['buttons'] = ['Edit']
