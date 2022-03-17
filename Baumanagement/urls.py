from django.urls import path

from . import views

urlpatterns = [
    path("", views.test_view),
    path("companies", views.companies),
    path("company/<int:id>", views.company),
    path("companies/<int:id>", views.role),
    path("projects", views.projects),
    path("project/<int:id>", views.project),
    path("contracts", views.contracts),
    path("payments", views.payments),
    path("bills", views.bills),
]
