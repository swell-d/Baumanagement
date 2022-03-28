from django.urls import path

from .views import views_bills, views_companies, views_delete, views_contracts, views_payments, views_projects

urlpatterns = [
    path("", views_projects.projects, name='index'),

    path("companies", views_companies.companies, name="companies"),
    path("companies/<int:id>", views_companies.companies_by_role, name="companies_by_role"),
    path("company/<int:id>", views_companies.company, name="companies_id"),

    path("projects", views_projects.projects, name="projects"),
    path("project/<int:id>", views_projects.project),
    path("project/<int:id>/payments", views_payments.project_payments),
    path("project/<int:id>/bills", views_bills.project_bills),

    path("contracts", views_contracts.contracts, name="contracts"),
    path("contract/<int:id>", views_contracts.contract),
    path("contract/<int:id>/payments", views_payments.contract_payments),
    path("contract/<int:id>/bills", views_bills.contract_bills),

    path("payments", views_payments.payments, name="payments"),
    path("payment/<int:id>", views_payments.payment),

    path("bills", views_bills.bills, name="bills"),
    path("bill/<int:id>", views_bills.bill),

    path("delete_file/<int:id>", views_delete.delete_file),

]


def get_urls():
    return [f'/{each.pattern}'.replace('<int:id>', '1') for each in urlpatterns]
