from django.urls import path

from . import views

urlpatterns = [
    # path('companies', views.companies_view, name='companies'),
    # path('companies_by_role', views.companies_by_role_view, name='companies_by_role'),
    path("companies", views.CompanyListView.as_view()),
    path("company_roles", views.CompanyRoleListView.as_view()),
]
