from django.contrib import admin

from Baumanagement.models.models_comments import Comment
from Baumanagement.models.models_company import CompanyRole, Company, Account, Currency, Contact
from Baumanagement.models.models_contracts import Contract, Payment, Bill, ContractTag
from Baumanagement.models.models_files import File
from Baumanagement.models.models_messages import MyMessage
from Baumanagement.models.models_products import Product, ProductCategory
from Baumanagement.models.models_projects import Project, ProjectTag
from Baumanagement.models.models_settings import Settings

admin.site.register(Currency)
admin.site.register(MyMessage)
admin.site.register(Settings)

admin.site.register(ProductCategory)
admin.site.register(Product)

admin.site.register(CompanyRole)
admin.site.register(Company)
admin.site.register(Account)
admin.site.register(Contact)

admin.site.register(ProjectTag)
admin.site.register(Project)

admin.site.register(ContractTag)
admin.site.register(Contract)
admin.site.register(Bill)
admin.site.register(Payment)

admin.site.register(File)
admin.site.register(Comment)
