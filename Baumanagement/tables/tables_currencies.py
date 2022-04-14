from Baumanagement.models.models_currency import Currency
from Baumanagement.tables.tables import MyTable, base_render


class CurrencyTable(MyTable):
    class Meta(MyTable.Meta):
        model = Currency
        fields = Currency.table_fields

    def render_code(self, record, value):
        return base_render(self, record, value)

    def render_symbol(self, record, value):
        return base_render(self, record, value)

    def render_rate(self, record, value):
        return base_render(self, record, value)
