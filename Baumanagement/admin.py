from django.contrib import admin

from .models import Company, CompanyRole, Project, Contract, Payment

admin.site.register(Company)
admin.site.register(CompanyRole)
admin.site.register(Project)
admin.site.register(Contract)
admin.site.register(Payment)
