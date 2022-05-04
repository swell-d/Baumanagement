from django.urls import path

from .views import views_products, views_productcategories

urlpatterns = [
    path("productcategories", views_productcategories.objects_table, name="productcategories"),
    path("productcategory/<int:id>", views_productcategories.object_table, name="productcategory_id"),

    path("products", views_products.objects_table, name="products"),
    path("product/<int:id>", views_products.object_table, name="product_id")
]
