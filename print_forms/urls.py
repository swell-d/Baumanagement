from django.urls import path

import print_forms.views

urlpatterns = [
    path("bill/<int:id>/html", print_forms.views.html, name="bill_id_html"),
    path("bill/<int:id>/xlsx", print_forms.views.xlsx, name="bill_id_xlsx"),
]
