from django.urls import path

import comments.views

urlpatterns = [
    path("comments", comments.views.objects_table, name="comments"),
    path("comment/<int:id>", comments.views.object_table, name="comment_id")
]
