from django.urls import path

import products.views
from products import views_productcategories

urlpatterns = [
    path("productcategories", views_productcategories.objects_table, name="productcategories"),
    path("productcategory/<int:id>", views_productcategories.object_table, name="productcategory_id"),

    path("products", products.views.objects_table, name="products"),
    path("product/<int:id>", products.views.object_table, name="product_id")
]
