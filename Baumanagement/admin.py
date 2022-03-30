from django.contrib import admin

from Baumanagement.models.models import Project, Contract, Payment, Bill
from Baumanagement.models.models_company import CompanyRole, Company
from Baumanagement.models.models_files import File

admin.site.register(CompanyRole)
admin.site.register(Company)
admin.site.register(Project)
admin.site.register(Contract)
admin.site.register(Bill)
admin.site.register(Payment)
admin.site.register(File)
