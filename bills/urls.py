from django.urls import path

import bills.views

urlpatterns = [
    path("bills", bills.views.objects_table, name="bills"),
    path("bill/<int:id>", bills.views.object_table, name="bill_id")
]
