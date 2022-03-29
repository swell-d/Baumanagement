from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_files import File


def delete_file(request, id):
    if request.method != 'POST':
        return HttpResponseNotFound('')
    file = File.objects.get(id=id)
    filename = file.name
    file.delete()
    messages.success(request, f'{filename} {_("deleted")}')
    return HttpResponse('')
