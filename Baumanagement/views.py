from django.shortcuts import render

from Baumanagement.models import Company, CompanyRole
from Baumanagement.tables import CompanyTable, CompanyRoleTable


def companies(request):
    context = {'table': CompanyTable(Company.objects.all()),
               'h1': 'Alle Unternehmen'}
    return render(request, 'Baumanagement/companies.html', context)


def role(request, id):
    context = {'table': CompanyTable(Company.objects.filter(role=id).all()),
               'h1': f'Rolle - {CompanyRole.objects.get(id=id).name}'}
    return render(request, 'Baumanagement/companies.html', context)


def company_roles(request):
    context = {'table': CompanyRoleTable(CompanyRole.objects.all()),
               'h1': 'Alle Rollen'}
    return render(request, 'Baumanagement/companies.html', context)


def test_view(request):
    data = [', '.join([each2.name for each2 in each.companies.all()]) for each in CompanyRole.objects.all()]
    context = {'data': data}
    return render(request, 'Baumanagement/test.html', context)
