from django.urls import path

import bills.views
import contracts.views
import payments.views
import projects.views
import projects.views_labels

urlpatterns = [
    path("projectlabels", projects.views_labels.objects_table, name="projectlabels"),
    path("projectlabel/<int:id>", projects.views_labels.object_table, name="projectlabel_id"),

    path("projects", projects.views.objects_table, name="projects"),
    path("project/<int:id>", projects.views.object_table, name="project_id"),
    path("project/<int:id>/contracts", contracts.views.project_contracts, name="project_id_contracts"),
    path("project/<int:id>/payments", payments.views.project_payments, name="project_id_payments"),
    path("project/<int:id>/bills", bills.views.project_bills, name="project_id_bills")
]
