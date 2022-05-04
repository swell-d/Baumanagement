from django.urls import path

import bank_accounts.views
import bills.views
import contacts.views
import contracts.views
import payments.views
from .views import views_companies, views_projects, \
    views_companyroles, views_currencies, views_projecttags, \
    views_products, views_productcategories

urlpatterns = [
    path("productcategories", views_productcategories.objects_table, name="productcategories"),
    path("productcategory/<int:id>", views_productcategories.object_table, name="productcategory_id"),

    path("products", views_products.objects_table, name="products"),
    path("product/<int:id>", views_products.object_table, name="product_id"),

    path("companyroles", views_companyroles.objects_table, name="companyroles"),
    path("companyrole/<int:id>", views_companyroles.object_table, name="companyrole_id"),

    path("companies", views_companies.objects_table, name="companies"),
    path("companies/<int:id>", views_companies.companies_by_role, name="companies_id"),
    path("company/<int:id>", views_companies.object_table, name="company_id"),
    path("company/<int:id>/accounts", bank_accounts.views.company_accounts, name="company_id_accounts"),
    path("company/<int:id>/contacts", contacts.views.company_contacts, name="company_id_contacts"),
    path("company/<int:id>/projects", views_projects.company_projects, name="company_id_projects"),
    path("company/<int:id>/contracts", contracts.views.company_contracts, name="company_id_contracts"),
    path("company/<int:id>/payments", payments.views.company_payments, name="company_id_payments"),
    path("company/<int:id>/bills", bills.views.company_bills, name="company_id_bills"),
    path("company/<int:id>/companies", views_companies.company_companies, name="company_id_companies"),

    path("currencies", views_currencies.objects_table, name="currencies"),
    path("currency/<int:id>", views_currencies.object_table, name="currency_id"),

    path("projectlabels", views_projecttags.objects_table, name="projectlabels"),
    path("projectlabel/<int:id>", views_projecttags.object_table, name="projectlabel_id"),

    path("projects", views_projects.objects_table, name="projects"),
    path("project/<int:id>", views_projects.object_table, name="project_id"),
    path("project/<int:id>/contracts", contracts.views.project_contracts, name="project_id_contracts"),
    path("project/<int:id>/payments", payments.views.project_payments, name="project_id_payments"),
    path("project/<int:id>/bills", bills.views.project_bills, name="project_id_bills"),
]
