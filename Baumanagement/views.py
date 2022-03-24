from django.shortcuts import render


def myrender(request, context):
    search = request.GET.get('search')
    template = 'Baumanagement/tables.html' if search is None else 'Baumanagement/maintable.html'
    context['url'] = request.path
    return render(request, template, context)
