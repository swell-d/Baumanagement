from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.abstract import add_search_field
from Baumanagement.models.models import Project, Contract
from Baumanagement.tables import ProjectTable, ContractTable
from Baumanagement.views.views import myrender, new_object_form, edit_object_form


def projects(request):
    context = {'titel1': _('All projects')}
    new_object_form(request, context, ProjectForm)

    queryset = Project.extra_fields(Project.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = ProjectTable(queryset, order_by="name", orderable=request.GET.get('search') is None)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def project(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Project")} - {project.name}', 'tables': []}
    edit_object_form(request, context, ProjectForm, project)

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
