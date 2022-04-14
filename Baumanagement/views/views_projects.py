from django import forms
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Company
from Baumanagement.models.models_projects import Project, ProjectTag
from Baumanagement.tables.tables_projects import ProjectTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table, get_base_context
from Baumanagement.views.views_bills import generate_bills_by_queryset, project_bills_qs
from Baumanagement.views.views_contracts import generate_contracts_by_queryset, project_contracts_qs
from Baumanagement.views.views_payments import generate_payments_by_queryset, project_payments_qs

baseClass = Project
tableClass = ProjectTable


class FormClass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(open=True)

    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def tags():
    html = f'<a href="" onclick="mainTableTag(&quot;?tag=&quot;);return false;">{_("All")}</a>, '
    html += ', '.join(
        f'#<a href="" onclick="mainTableTag(&quot;?tag={tag.id}&quot;);return false;">{tag.name}</a>'
        for tag in ProjectTag.objects.order_by('name') if tag.count > 0)
    html += ' &#9881;<a href="' + reverse('projecttags') + '">' + _('Manage labels') + '</a>'
    return format_html(html)


def objects_table(request):
    context = get_base_context(request)
    context['tags1'] = tags()
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    project = queryset.first()

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_projects', args=[project.company.id]),
                               'text': project.company.name},
                              {'text': queryset.first().name}]

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)

    contracts = project_contracts_qs(project)
    generate_contracts_by_queryset(request, context, contracts)

    bills = project_bills_qs(project)
    generate_bills_by_queryset(request, context, bills)

    payments = project_payments_qs(project)
    generate_payments_by_queryset(request, context, payments)

    return myrender(request, context)


def company_projects(request, id):
    context = get_base_context(request)
    company = Company.objects.get(id=id)
    context['tags1'] = tags()
    queryset = company.projects.all()

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': company.name}]

    form = FormClass()
    form.fields["company"].initial = company
    form.fields['company'].queryset = Company.objects.filter(id=id)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_projects_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
