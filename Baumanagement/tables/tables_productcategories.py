from django.urls import reverse
from django.utils.html import format_html

from Baumanagement.models.models_products import ProductCategory
from Baumanagement.tables.tables import MyTable, modal


class ProductCategoryTable(MyTable):
    class Meta(MyTable.Meta):
        model = ProductCategory
        fields = ProductCategory.table_fields

    def render_name(self, record, value):
        return format_html(
            f'''<strong><a href="{modal if self.object_table else reverse('productcategory_id', args=[record.id])}">
            {record}</a></strong>''')
