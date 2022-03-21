import django_filters

from Baumanagement.models import Bill


class BillFilter(django_filters.FilterSet):
    class Meta:
        model = Bill
        fields = Bill.fields()
