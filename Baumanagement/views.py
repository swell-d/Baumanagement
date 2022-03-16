from django.shortcuts import render
from django_tables2 import RequestConfig

from Baumanagement.models import Company, CompanyRole
from Baumanagement.tables import CompanyTable, CompanyRoleTable


def companies(request):
    table = CompanyTable(Company.objects.all())
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Unternehmen'}
    return render(request, 'Baumanagement/companies.html', context)


def role(request, id):
    table = CompanyTable(Company.objects.filter(role=id).all())
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': f'Rolle - {CompanyRole.objects.get(id=id).name}'}
    return render(request, 'Baumanagement/companies.html', context)


def company_roles(request):
    table = CompanyRoleTable(CompanyRole.objects.all())
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Rollen'}
    return render(request, 'Baumanagement/companies.html', context)


def test_view(request):
    data = [', '.join([each2.name for each2 in each.companies.all()]) for each in CompanyRole.objects.all()]
    context = {'data': data}
    return render(request, 'Baumanagement/test.html', context)
