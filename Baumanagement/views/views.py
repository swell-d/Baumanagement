from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from Baumanagement.models import File


@login_required
def myrender(request, context):
    search = request.GET.get('search')
    template = 'Baumanagement/tables.html' if search is None else 'Baumanagement/maintable.html'
    return render(request, template, context)


def upload_files(request, *args, **kwargs):
    for file in request.FILES.getlist('file'):
        file_instance = File(name=file.name, file=file, **kwargs)
        file_instance.save()
        messages.success(request, f'{file.name} {_("uploaded")}')
