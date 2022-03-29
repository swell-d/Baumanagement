from django.urls import path

from .views import views_bills, views_companies, views_delete, views_contracts, views_payments, views_projects

urlpatterns = [
    path("", views_projects.projects, name='index'),

    path("companies", views_companies.companies, name="companies"),
    path("companies/<int:id>", views_companies.companies_by_role, name="companies_id"),
    path("company/<int:id>", views_companies.company, name="company_id"),

    path("projects", views_projects.projects, name="projects"),
    path("project/<int:id>", views_projects.project, name="project_id"),
    path("project/<int:id>/payments", views_payments.project_payments, name="project_id_payments"),
    path("project/<int:id>/bills", views_bills.project_bills, name="project_id_bills"),

    path("contracts", views_contracts.contracts, name="contracts"),
    path("contract/<int:id>", views_contracts.contract, name="contract_id"),
    path("contract/<int:id>/payments", views_payments.contract_payments, name="contract_id_payments"),
    path("contract/<int:id>/bills", views_bills.contract_bills, name="contract_id_bills"),

    path("payments", views_payments.payments, name="payments"),
    path("payment/<int:id>", views_payments.payment, name="payment_id"),

    path("bills", views_bills.bills, name="bills"),
    path("bill/<int:id>", views_bills.bill, name="bill_id"),

    path("delete_file/<slug:class_name>/<int:id>", views_delete.delete_file, name="delete_file_id"),

]


def get_urls():
    urls = [f'/de/{each.pattern}'.replace('<int:id>', '1').replace('<slug:class_name>', 'File') for each in urlpatterns]
    urls += [f'/en/{each.pattern}'.replace('<int:id>', '1') for each in urlpatterns]
    return urls
