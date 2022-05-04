from django.urls import path

import notifications.views

urlpatterns = [
    path("notifications", notifications.views.objects_table, name="notifications"),
    path("notification/<int:id>", notifications.views.object_table, name="notification_id")
]
