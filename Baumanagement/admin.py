from django.contrib import admin

from Baumanagement.models.models import Contract, Payment, Bill
from Baumanagement.models.models_projects import Project, ProjectType
from Baumanagement.models.models_comments import Comment
from Baumanagement.models.models_company import CompanyRole, Company, Account, Currency, Contact
from Baumanagement.models.models_files import File

admin.site.register(CompanyRole)
admin.site.register(ProjectType)
admin.site.register(Company)
admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Contact)
admin.site.register(Project)
admin.site.register(Contract)
admin.site.register(Bill)
admin.site.register(Payment)
admin.site.register(File)
admin.site.register(Comment)
