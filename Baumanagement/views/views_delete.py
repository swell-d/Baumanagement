from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_files import File
from Baumanagement.views.views import my404


def delete_file(request, id):
    if request.method != 'POST':
        return HttpResponseNotFound(my404(request))
    file = File.objects.get(id=id)
    filename = file.name
    file.delete()
    messages.success(request, f'{filename} {_("deleted")}')
    return HttpResponse('')
