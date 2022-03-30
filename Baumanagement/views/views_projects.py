from django.contrib import messages
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.abstract import add_search_field
from Baumanagement.models.models import Project, Contract
from Baumanagement.tables import ProjectTable, ContractTable
from Baumanagement.views.views import myrender, upload_files


def projects(request):
    context = {'titel1': _('All projects')}
    form_new_project(request, context)

    queryset = Project.extra_fields(Project.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = ProjectTable(queryset, order_by="name", orderable=request.GET.get('search') is None)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def project(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Project")} - {project.name}', 'tables': []}
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
        context['tables'].append({'table': table, 'titel': _("Contracts")})

    return myrender(request, context)


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = Project.form_fields


def form_new_project(request, context):
    if request.method == 'POST':
        formset = ProjectForm(request.POST, request.FILES)
        if formset.is_valid():
            new_object = Project(**formset.cleaned_data)
            new_object.save()
            messages.success(request, f'{new_object.name} {_("created")}')
            upload_files(request, new_object)
    context['form'] = ProjectForm()
    context['files_form'] = []
    context['buttons'] = ['New']


def form_edit_project(request, context, project):
    if request.method == 'POST':
        formset = ProjectForm(request.POST, request.FILES, instance=project)
        if formset.is_valid():
            project.save()
            messages.success(request, f'{project.name} {_("changed")}')
            upload_files(request, project)
    context['form'] = ProjectForm(instance=project)
    context['files_form'] = project.files
    context['buttons'] = ['Edit']
