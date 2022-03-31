from django.urls import path

from .views import views_bills, views_companies, views_delete, views_contracts, views_payments, views_projects, \
    views_accounts, views_comments

urlpatterns = [
    path("", views_projects.objects_table, name='index'),

    path("companies", views_companies.objects_table, name="companies"),
    path("companies/<int:id>", views_companies.companies_by_role, name="companies_id"),
    path("company/<int:id>", views_companies.object_table, name="company_id"),

    path("accounts", views_accounts.objects_table, name="accounts"),
    path("account/<int:id>", views_accounts.object_table, name="account_id"),

    path("projects", views_projects.objects_table, name="projects"),
    path("project/<int:id>", views_projects.object_table, name="project_id"),
    path("project/<int:id>/payments", views_payments.project_payments, name="project_id_payments"),
    path("project/<int:id>/bills", views_bills.project_bills, name="project_id_bills"),

    path("contracts", views_contracts.objects_table, name="contracts"),
    path("contract/<int:id>", views_contracts.object_table, name="contract_id"),
    path("contract/<int:id>/payments", views_payments.contract_payments, name="contract_id_payments"),
    path("contract/<int:id>/bills", views_bills.contract_bills, name="contract_id_bills"),

    path("payments", views_payments.objects_table, name="payments"),
    path("payment/<int:id>", views_payments.object_table, name="payment_id"),

    path("bills", views_bills.objects_table, name="bills"),
    path("bill/<int:id>", views_bills.object_table, name="bill_id"),

    path("comments", views_comments.objects_table, name="comments"),
    path("comment/<int:id>", views_comments.object_table, name="comment_id"),

    path("delete_file/<int:id>", views_delete.delete_file, name="delete_file_id"),

]


def get_urls():
    urls = [f'/de/{each.pattern}'.replace('<int:id>', '1') for each in urlpatterns]
    urls += [f'/en/{each.pattern}'.replace('<int:id>', '1') for each in urlpatterns]
    return urls
