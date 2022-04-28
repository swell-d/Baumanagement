from django.http import HttpResponse, HttpResponseNotFound
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_files import File
from Baumanagement.models.models_messages import MyMessage
from Baumanagement.views.views import my404


def delete_file(request, id):
    if request.method != 'POST':
        return my404(request, None)
    file = File.objects.get(id=id)
    filename = file.name
    verbose_name = file.verbose_name()
    file.delete()

    MyMessage.message(
        request, f'{verbose_name} "{filename}" ' + _("deleted"), 'SUCCESS'
    )
    return HttpResponse('')
