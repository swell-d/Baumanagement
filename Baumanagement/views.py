from django.shortcuts import render
from django.views.generic import ListView

from Baumanagement.models import Company, CompanyRole


class CompanyListView(ListView):
    model = Company
    template_name = 'Baumanagement/CompanyList.html'


class CompanyRoleListView(ListView):
    model = CompanyRole
    template_name = 'Baumanagement/CompanyRoleList.html'


def companies_by_role_view(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'Baumanagement/CompaniesByRole.html', context)


def companies_view(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'Baumanagement/Companies.html', context)
