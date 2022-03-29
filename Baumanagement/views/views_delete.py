from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_files import FilesClasses


def delete_file(request, class_name, id):
    if request.method != 'POST':
        return HttpResponseNotFound('')
    file = FilesClasses[class_name].objects.get(id=id)
    filename = file.name
    file.delete()
    messages.success(request, f'{filename} {_("deleted")}')
    return HttpResponse('')
