from django.urls import path

import bills.views
import contracts.views
import payments.views
from .views import views_projects, \
    views_projecttags, \
    views_products, views_productcategories

urlpatterns = [
    path("productcategories", views_productcategories.objects_table, name="productcategories"),
    path("productcategory/<int:id>", views_productcategories.object_table, name="productcategory_id"),

    path("products", views_products.objects_table, name="products"),
    path("product/<int:id>", views_products.object_table, name="product_id"),

    path("projectlabels", views_projecttags.objects_table, name="projectlabels"),
    path("projectlabel/<int:id>", views_projecttags.object_table, name="projectlabel_id"),

    path("projects", views_projects.objects_table, name="projects"),
    path("project/<int:id>", views_projects.object_table, name="project_id"),
    path("project/<int:id>/contracts", contracts.views.project_contracts, name="project_id_contracts"),
    path("project/<int:id>/payments", payments.views.project_payments, name="project_id_payments"),
    path("project/<int:id>/bills", bills.views.project_bills, name="project_id_bills"),
]
