from django.shortcuts import render


def myrender(request, context):
    search = request.GET.get('search')
    template = 'Baumanagement/maintable.html' if search is not None else 'Baumanagement/tables.html'
    return render(request, template, context)
