from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django_tables2 import RequestConfig

from Baumanagement.forms_bills import BillForm
from Baumanagement.models import Bill
from Baumanagement.tables import BillTable


def bills(request):
    search = request.GET.get('search')
    if search is not None:
        text_fields = 'contract__project__name', 'contract__company__name', 'contract__name', \
                      'name', 'amount_netto', 'vat', 'amount_brutto'
        queries = [Q(**{f'{field}__icontains': search}) for field in text_fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        table1 = BillTable(Bill.objects.filter(qs), order_by="id")
    else:
        table1 = BillTable(Bill.objects.all(), order_by="id")

    RequestConfig(request).configure(table1)

    context = {'titel1': 'Alle Rechnungen', 'table1': table1, 'search': search, 'url': request.path}
    return render(request,
                  'Baumanagement/maintable.html' if search is not None else 'Baumanagement/tables.html',
                  context)


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
