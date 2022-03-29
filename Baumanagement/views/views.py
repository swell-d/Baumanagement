from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_files import File


@login_required
def myrender(request, context):
    template = 'tables.html' if request.GET.get('search') is None else 'maintable.html'
    return render(request, template, context)


def upload_files(request, object):
    for file in request.FILES.getlist('file'):
        file_instance = File.objects.create(name=file.name, file=file)
        object.file_ids.append(file_instance.id)
        object.save()
        messages.success(request, f'{file.name} {_("uploaded")}')
