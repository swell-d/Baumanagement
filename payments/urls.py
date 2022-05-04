from django.urls import path

import payments.views

urlpatterns = [
    path("payments", payments.views.objects_table, name="payments"),
    path("payment/<int:id>", payments.views.object_table, name="payment_id")
]
