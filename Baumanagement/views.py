from django.shortcuts import render


def myrender(request, context):
    search = request.GET.get('search')
    template = 'Baumanagement/maintable.html' if search is not None else 'Baumanagement/tables.html'
    context['url'] = request.path
    return render(request, template, context)
