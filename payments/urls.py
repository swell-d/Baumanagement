from django.urls import path

import payments.views
import payments.views_labels

urlpatterns = [
    path("paymentlabels", payments.views_labels.objects_table, name="paymentlabels"),
    path("paymentlabel/<int:id>", payments.views_labels.object_table, name="paymentlabel_id"),

    path("payments", payments.views.objects_table, name="payments"),
    path("payment/<int:id>", payments.views.object_table, name="payment_id")
]
