from django.urls import path

import files.views

urlpatterns = [
    path("delete_file/<int:id>", files.views.delete_file, name="delete_file_id")
]
