import os

from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from Baumanagement.models import File


def delete_file(request, id):
    file = File.objects.get(id=id)
    filename = file.name
    os.remove(file.file.path)
    file.delete()
    messages.success(request, f'{filename} {_("deleted")}')
    return HttpResponse('')
