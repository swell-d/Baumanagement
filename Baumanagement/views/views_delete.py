from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_files import File
from Baumanagement.models.models_messages import MyMessage


def delete_file(request, id):
    if request.method != 'POST':
        raise Http404
    file = get_object_or_404(File, id=id)
    filename = file.name
    verbose_name = file.verbose_name()
    file.delete()

    MyMessage.message(
        request, f'{verbose_name} "{filename}" ' + _("deleted"), 'SUCCESS'
    )
    return HttpResponse('')
