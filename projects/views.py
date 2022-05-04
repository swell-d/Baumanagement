from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from bills.views import project_bills_qs, generate_bills_by_queryset
from companies.models import Company
from contracts.views import project_contracts_qs, generate_contracts_by_queryset
from main.views import superuser_required, get_base_context, generate_objects_table, myrender, generate_object_table, \
    generate_next_objects_table
from payments.views import project_payments_qs, generate_payments_by_queryset
from projects.models import Project
from projects.models_labels import ProjectLabel
from projects.tables import ProjectTable

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
    html = f'<a href="" onclick="mainTableLabel(&quot;&quot;);return false;">{_("All")}</a>, '
    html += ', '.join(
        f'#<a href="" onclick="mainTableLabel(&quot;{tag.id}&quot;);return false;">{str(tag)}</a>'
        for tag in ProjectLabel.objects.order_by('name') if tag.count > 0)
    html += ' &#9881;<a href="' + reverse('projectlabels') + '">' + _('Manage labels') + '</a>'
    return format_html(html)


@superuser_required
@login_required
def objects_table(request):
    context = get_base_context(request)
    context['tags1'] = tags()
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


@login_required
def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    if queryset.first() is None:
        raise Http404
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


@login_required
def company_projects(request, id):
    context = get_base_context(request)
    company = get_object_or_404(Company, id=id)
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