from django.urls import path

from first_run import views

urlpatterns = [
    path("first_run", views.first_run, name='first_run'),
]
