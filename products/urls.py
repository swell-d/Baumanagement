from django.urls import path

import products.views
import products.views_labels

urlpatterns = [
    path("productcategories", products.views_labels.objects_table, name="productcategories"),
    path("productcategory/<int:id>", products.views_labels.object_table, name="productcategory_id"),

    path("products", products.views.objects_table, name="products"),
    path("product/<int:id>", products.views.object_table, name="product_id")
]
