from currencies.models import Currency
from main.tables import MyTable, base_render


class CurrencyTable(MyTable):
    class Meta(MyTable.Meta):
        model = Currency
        fields = Currency.table_fields

    def render_symbol(self, record, value):
        return base_render(self, record, value)

    def render_rate(self, record, value):
        return base_render(self, record, value)
