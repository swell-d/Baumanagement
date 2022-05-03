from django.urls import path

import structure.views

urlpatterns = [
    path("structure", structure.views.structure, name='structure')
]
