from django.urls import path

import bills.views
import contracts.views
import contracts.views_labels
import payments.views

urlpatterns = [
    path("contractlabels", contracts.views_labels.objects_table, name="contractlabels"),
    path("contractlabel/<int:id>", contracts.views_labels.object_table, name="contractlabel_id"),

    path("contracts", contracts.views.objects_table, name="contracts"),
    path("contract/<int:id>", contracts.views.object_table, name="contract_id"),
    path("contract/<int:id>/payments", payments.views.contract_payments, name="contract_id_payments"),
    path("contract/<int:id>/bills", bills.views.contract_bills, name="contract_id_bills")
]
