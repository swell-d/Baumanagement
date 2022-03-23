from django.urls import path

from . import views_bills
from . import views_companies
from . import views_contracts
from . import views_payments
from . import views_projects

urlpatterns = [
    path("", views_projects.projects),

    path("companies", views_companies.companies),
    path("companies/<int:id>", views_companies.companies_by_role),
    path("company/<int:id>", views_companies.company),

    path("projects", views_projects.projects),
    path("project/<int:id>", views_projects.project),
    path("project/<int:id>/payments", views_projects.project_payments),
    path("project/<int:id>/bills", views_projects.project_bills),

    path("contracts", views_contracts.contracts),
    path("contract/<int:id>", views_contracts.contract),
    path("contract/<int:id>/payments", views_contracts.contract_payments),
    path("contract/<int:id>/bills", views_contracts.contract_bills),

    path("payments", views_payments.payments),
    path("payment/<int:id>", views_payments.payment),

    path("bills", views_bills.bills),
    path("bill/<int:id>", views_bills.bill),

]


def get_urls():
    return [f'/{each.pattern}'.replace('<int:id>', '1') for each in urlpatterns]
