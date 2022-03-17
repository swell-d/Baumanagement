from django.urls import path

from . import views

urlpatterns = [
    path("", views.test_view),
    path("companies", views.companies),
    path("companies/<int:id>", views.role),
    path("projects", views.projects),
    path("contracts", views.contracts),
    path("payments", views.payments),
]
