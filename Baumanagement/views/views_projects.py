from django import forms
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Company
from Baumanagement.models.models_contracts import Bill, Payment
from Baumanagement.models.models_projects import Project, ProjectTag
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


def tags():
    html = f'<a href="" onclick="mainTableTag(&quot;?tag=&quot;);return false;">{_("All")}</a>, '
    html += ', '.join(
        f'#<a href="" onclick="mainTableTag(&quot;?tag={tag.id}&quot;);return false;">{tag.name}</a>'
        for tag in ProjectTag.objects.order_by('name') if tag.count > 0)
    return format_html(html)


def objects_table(request):
    context = {}
    context['tags1'] = tags()
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    context = {'tables': []}
    queryset = baseClass.objects.filter(id=id)
    project = queryset.first()

    context['breadcrumbs'] = [{'link': reverse(baseClass.url), 'text': _("All")},
                              {'link': reverse('company_id_projects', args=[project.company.id]),
                               'text': project.company.name},
                              {'text': queryset.first().name}]

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
    context = {}
    queryset = company.projects.all()

    context['breadcrumbs'] = [{'link': reverse(baseClass.url), 'text': _("All")},
                              {'text': company.name}]

    form = FormClass()
    form.fields["company"].initial = company
    form.fields['company'].queryset = Company.objects.filter(id=id)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_projects_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)


def projects_by_tag(request, id):
    tag = ProjectTag.objects.get(id=id)
    context = {}
    queryset = baseClass.objects.filter(tag=id)

    context['breadcrumbs'] = [{'link': reverse(baseClass.url), 'text': _("All")},
                              {'text': tag.name}]

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    context['tags1'] = tags()
    return myrender(request, context)
