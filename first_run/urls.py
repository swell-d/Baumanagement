from django.urls import path

import first_run.views

urlpatterns = [
    path("first_run", first_run.views.first_run, name='first_run'),
]
