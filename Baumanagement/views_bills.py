from django.shortcuts import render
from django.views import View
from django_tables2 import RequestConfig

from Baumanagement.filters import BillFilter
from Baumanagement.forms_bills import BillForm
from Baumanagement.models import Bill
from Baumanagement.tables import BillTable


def bills(request):
    filter = BillFilter(request.GET, queryset=Bill.objects.all())
    table1 = BillTable(filter.qs, order_by="id")
    RequestConfig(request).configure(table1)

    context = {'titel1': 'Alle Rechnungen', 'table1': table1, 'filter': filter}
    return render(request, 'Baumanagement/tables.html', context)


def bill(request, id):
    bill = Bill.objects.get(id=id)

    table1 = BillTable(Bill.objects.filter(id=id))
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Rechnung - {bill.name}', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


class BillView(View):
    def get(self, request, *args, **kwarg):
        form = BillForm()
        return render(request, 'Baumanagement/tables.html', context={'form': form})

    def post(self, request, *args, **kwarg):
        pass
