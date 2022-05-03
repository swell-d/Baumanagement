from django.shortcuts import render


def structure(request):
    return render(request, 'structure/structure.html')
