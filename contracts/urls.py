from django.urls import path

import contracts.views
from Baumanagement.views import views_payments, views_bills
from contracts import views_contracttags

urlpatterns = [
    path("contractlabels", views_contracttags.objects_table, name="contractlabels"),
    path("contractlabel/<int:id>", views_contracttags.object_table, name="contractlabel_id"),

    path("contracts", contracts.views.objects_table, name="contracts"),
    path("contract/<int:id>", contracts.views.object_table, name="contract_id"),
    path("contract/<int:id>/payments", views_payments.contract_payments, name="contract_id_payments"),
    path("contract/<int:id>/bills", views_bills.contract_bills, name="contract_id_bills")
]
