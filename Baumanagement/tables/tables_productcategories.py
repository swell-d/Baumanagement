from Baumanagement.models.models_products import ProductCategory
from Baumanagement.tables.tables import MyTable


class ProductCategoryTable(MyTable):
    class Meta(MyTable.Meta):
        model = ProductCategory
        fields = ProductCategory.table_fields
