from django.shortcuts import render
from django.http import HttpResponse

from Baumanagement.models import Company, CompanyRole


def index(request):
    companies = Company.objects.all()
    context = {'companies': companies}

    return render(request, 'Baumanagement/CompaniesByRole.html', context)
