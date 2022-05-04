from django.urls import path

import bank_accounts.views
import bills.views
import companies.views
import contacts.views
import contracts.views
import payments.views
from Baumanagement.views import views_projects
from companies import views_companyroles

urlpatterns = [
    path("companyroles", views_companyroles.objects_table, name="companyroles"),
    path("companyrole/<int:id>", views_companyroles.object_table, name="companyrole_id"),

    path("companies", companies.views.objects_table, name="companies"),
    path("companies/<int:id>", companies.views.companies_by_role, name="companies_id"),
    path("company/<int:id>", companies.views.object_table, name="company_id"),
    path("company/<int:id>/accounts", bank_accounts.views.company_accounts, name="company_id_accounts"),
    path("company/<int:id>/contacts", contacts.views.company_contacts, name="company_id_contacts"),
    path("company/<int:id>/projects", views_projects.company_projects, name="company_id_projects"),
    path("company/<int:id>/contracts", contracts.views.company_contracts, name="company_id_contracts"),
    path("company/<int:id>/payments", payments.views.company_payments, name="company_id_payments"),
    path("company/<int:id>/bills", bills.views.company_bills, name="company_id_bills"),
    path("company/<int:id>/companies", companies.views.company_companies, name="company_id_companies")
]
