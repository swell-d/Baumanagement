from django.urls import path

import bills.views
import bills.views_labels

urlpatterns = [
    path("billlabels", bills.views_labels.objects_table, name="billlabels"),
    path("billlabel/<int:id>", bills.views_labels.object_table, name="billlabel_id"),

    path("bills", bills.views.objects_table, name="bills"),
    path("bill/<int:id>", bills.views.object_table, name="bill_id")
]
