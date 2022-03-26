from django.contrib import messages
from django.shortcuts import redirect

from Baumanagement.models import File


def delete_file(request, id):
    url = request.GET.get('next', '/')
    file = File.objects.get(id=id)  # ToDo delete file not only object
    filename = file.name
    file.delete()
    messages.success(request, f'{filename} entfernt')

    return redirect(url)
