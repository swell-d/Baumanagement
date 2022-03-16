from django.urls import path

from . import views

urlpatterns = [
    path("", views.test_view),
    path("companies", views.companies),
    path("company_roles", views.company_roles),
    path("role/<int:id>", views.role),
    path("projects", views.projects),
    path("contracts", views.contracts),
]
