from django.urls import path

from .views import views_bills, views_companies, views_delete, views_contracts, views_payments, views_projects, \
    views_accounts, views_comments, views_companyroles, views_currencies, views_contacts, views_projecttags, \
    views_contracttags, views, views_products, views_productcategories, views_messages

urlpatterns = [
    path("", views_projects.objects_table, name='index'),
    path("structure", views.structure, name='structure'),

    path("productcategories", views_productcategories.objects_table, name="productcategories"),
    path("productcategory/<int:id>", views_productcategories.object_table, name="productcategory_id"),

    path("products", views_products.objects_table, name="products"),
    path("product/<int:id>", views_products.object_table, name="product_id"),

    path("companyroles", views_companyroles.objects_table, name="companyroles"),
    path("companyrole/<int:id>", views_companyroles.object_table, name="companyrole_id"),

    path("companies", views_companies.objects_table, name="companies"),
    path("companies/<int:id>", views_companies.companies_by_role, name="companies_id"),
    path("company/<int:id>", views_companies.object_table, name="company_id"),
    path("company/<int:id>/accounts", views_accounts.company_accounts, name="company_id_accounts"),
    path("company/<int:id>/contacts", views_contacts.company_contacts, name="company_id_contacts"),
    path("company/<int:id>/projects", views_projects.company_projects, name="company_id_projects"),
    path("company/<int:id>/contracts", views_contracts.company_contracts, name="company_id_contracts"),
    path("company/<int:id>/payments", views_payments.company_payments, name="company_id_payments"),
    path("company/<int:id>/bills", views_bills.company_bills, name="company_id_bills"),
    path("company/<int:id>/companies", views_companies.company_companies, name="company_id_companies"),

    path("currencies", views_currencies.objects_table, name="currencies"),
    path("currency/<int:id>", views_currencies.object_table, name="currency_id"),

    path("accounts", views_accounts.objects_table, name="accounts"),
    path("account/<int:id>", views_accounts.object_table, name="account_id"),
    path("account/<int:id>/payments", views_payments.account_payments, name="account_id_payments"),

    path("contacts", views_contacts.objects_table, name="contacts"),
    path("contact/<int:id>", views_contacts.object_table, name="contact_id"),

    path("projecttags", views_projecttags.objects_table, name="projecttags"),
    path("projecttag/<int:id>", views_projecttags.object_table, name="projecttag_id"),

    path("projects", views_projects.objects_table, name="projects"),
    path("project/<int:id>", views_projects.object_table, name="project_id"),
    path("project/<int:id>/contracts", views_contracts.project_contracts, name="project_id_contracts"),
    path("project/<int:id>/payments", views_payments.project_payments, name="project_id_payments"),
    path("project/<int:id>/bills", views_bills.project_bills, name="project_id_bills"),

    path("contracttags", views_contracttags.objects_table, name="contracttags"),
    path("contracttag/<int:id>", views_contracttags.object_table, name="contracttag_id"),

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

    path("messages", views_messages.objects_table, name="messages"),
    path("message/<int:id>", views_messages.object_table, name="message_id"),

]


def get_urls():
    urls = [f'/de/{each.pattern}'.replace('<int:id>', '1') for each in urlpatterns]
    urls += [f'/en/{each.pattern}'.replace('<int:id>', '1') for each in urlpatterns]
    return urls
