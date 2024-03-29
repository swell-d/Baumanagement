from django.urls import path

import bank_accounts.views
import bills.views
import companies.views
import companies.views_labels
import contacts.views
import contracts.views
import payments.views
import projects.views

urlpatterns = [
    path("companylabels", companies.views_labels.objects_table, name="companylabels"),
    path("companylabel/<int:id>", companies.views_labels.object_table, name="companylabel_id"),

    path("companies", companies.views.objects_table, name="companies"),
    path("company/<int:id>", companies.views.object_table, name="company_id"),
    path("company/<int:id>/accounts", bank_accounts.views.company_accounts, name="company_id_accounts"),
    path("company/<int:id>/contacts", contacts.views.company_contacts, name="company_id_contacts"),
    path("company/<int:id>/projects", projects.views.company_projects, name="company_id_projects"),
    path("company/<int:id>/contracts", contracts.views.company_contracts, name="company_id_contracts"),
    path("company/<int:id>/payments", payments.views.company_payments, name="company_id_payments"),
    path("company/<int:id>/bills", bills.views.company_bills, name="company_id_bills"),
    path("company/<int:id>/companies", companies.views.company_companies, name="company_id_companies")
]
