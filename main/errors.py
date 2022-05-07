from django.http import HttpResponseNotFound
from django.shortcuts import render


def my404(request, exception):
    return HttpResponseNotFound(render(request, 'errors/404.html'))
