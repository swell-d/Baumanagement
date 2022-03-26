import os

from django.contrib import messages
from django.shortcuts import redirect

from Baumanagement.models import File


def delete_file(request, id):
    file = File.objects.get(id=id)
    filename = file.name
    os.remove(file.file.path)
    file.delete()
    messages.success(request, f'{filename} gelöscht')
    return redirect(request.GET.get('next', '/'))
