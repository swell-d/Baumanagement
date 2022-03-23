from django.views import View
from django_tables2 import RequestConfig

from Baumanagement.forms_bills import BillForm
from Baumanagement.models import Bill, filter_queryset
from Baumanagement.tables import BillTable
from Baumanagement.views import myrender


def bills(request):
    queryset = Bill.objects.all()
    queryset = filter_queryset(queryset, request)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Rechnungen', 'table1': table1, 'search_field': True}
    return myrender(request, context)


def bill(request, id):
    bill = Bill.objects.get(id=id)
    table1 = BillTable(Bill.objects.filter(id=id))
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Rechnung - {bill.name}', 'table1': table1}
    return myrender(request, context)


class BillView(View):
    def get(self, request, *args, **kwarg):
        form = BillForm()
        context = {'form': form}
        return myrender(request, context)

    def post(self, request, *args, **kwarg):
        pass
