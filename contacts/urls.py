from django.urls import path

import contacts.views

urlpatterns = [
    path("contacts", contacts.views.objects_table, name="contacts"),
    path("contact/<int:id>", contacts.views.object_table, name="contact_id")
]
