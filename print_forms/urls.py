from django.urls import path

from print_forms import views

urlpatterns = [
    path("bill/<int:id>/html", views.html, name="bill_id_html"),
    path("bill/<int:id>/xlsx", views.xlsx, name="bill_id_xlsx"),
]
