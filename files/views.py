from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from files.models import File
from notifications.models import Notification


@login_required
def delete_file(request, id):
    if request.method != 'POST':
        raise Http404
    file = get_object_or_404(File, id=id)
    filename = file.name
    verbose_name = file.verbose_name()
    file.delete()

    Notification.message(
        request, f'{verbose_name} "{filename}" ' + _("deleted"), 'SUCCESS'
    )
    return HttpResponse('')
