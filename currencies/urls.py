from django.urls import path

import currencies.views

urlpatterns = [
    path("currencies", currencies.views.objects_table, name="currencies"),
    path("currency/<int:id>", currencies.views.object_table, name="currency_id")
]
