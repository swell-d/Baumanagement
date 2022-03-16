from django.shortcuts import render
from django_tables2 import RequestConfig

from Baumanagement.models import Company, CompanyRole, Project
from Baumanagement.tables import CompanyTable, CompanyRoleTable, ProjectTable


def companies(request):
    table = CompanyTable(Company.objects.all(), order_by="name")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Unternehmen'}
    return render(request, 'Baumanagement/companies.html', context)


def role(request, id):
    table = CompanyTable(Company.objects.filter(role=id).all(), order_by="name")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': f'Rolle - {CompanyRole.objects.get(id=id).name}'}
    return render(request, 'Baumanagement/companies.html', context)


def company_roles(request):
    table = CompanyRoleTable(CompanyRole.objects.all(), order_by="name")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Rollen'}
    return render(request, 'Baumanagement/companies.html', context)


def projects(request):
    table = ProjectTable(Project.objects.all(), order_by="name")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Projekte'}
    return render(request, 'Baumanagement/companies.html', context)


def test_view(request):
    # data = [', '.join([each2.name for each2 in each.companies.all()]) for each in CompanyRole.objects.all()]
    context = {'data': []}
    return render(request, 'Baumanagement/test.html', context)
