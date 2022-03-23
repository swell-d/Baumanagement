from django.forms import ModelForm
from django_tables2 import RequestConfig

from Baumanagement.models import Bill, filter_queryset
from Baumanagement.tables import BillTable
from Baumanagement.views import myrender


def bills(request):
    queryset = Bill.objects
    queryset = Bill.extra_fields(queryset)
    queryset = filter_queryset(queryset, request)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Rechnungen', 'table1': table1, 'search_field': True}
    return myrender(request, context)


def bill(request, id):
    bill = Bill.objects.get(id=id)

    if request.method == 'POST':
        formset = BillForm(request.POST, request.FILES, instance=bill)
        if formset.is_valid():
            bill.save()

    queryset = Bill.objects.filter(id=id)
    queryset = Bill.extra_fields(queryset)
    table1 = BillTable(queryset)
    RequestConfig(request).configure(table1)

    form = BillForm(instance=bill)

    context = {'titel1': f'Rechnung - {bill.name}', 'table1': table1, 'form': form}
    return myrender(request, context)


class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = ['open', 'name', 'contract', 'date', 'amount_netto', 'vat', 'amount_brutto']
