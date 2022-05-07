from django.shortcuts import redirect, render
from django_tables2.export import TableExport

from main.forms import EmptyForm


def myrender(request, context):
    if request.POST \
            and not context.get('form', EmptyForm()).errors \
            and not context.get('productsform', EmptyForm()).errors:
        return redirect(request.path)

    export_format = request.GET.get("_export", None)
    if export_format and TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, context['table1'])
        return exporter.response("table.{}".format(export_format))

    template = 'tables/tables.html' if not request.GET else 'tables/maintable.html'
    return render(request, template, context)
