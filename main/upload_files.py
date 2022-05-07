from django.utils.translation import gettext_lazy as _

from files.models import File
from notifications.models import Notification


def upload_files(request, new_object):
    for file in request.FILES.getlist('file'):
        if str(file.name).endswith('.py'):
            continue
        file_instance = File.objects.create(name=file.name, file=file)
        new_object.file_ids.append(file_instance.id)
        new_object.save()

        verbose_name = file_instance.verbose_name()
        link = file_instance.file.url
        Notification.message(
            request, f'{verbose_name} "<a href="{link}">{file_instance.name}</a>" ' + _("uploaded"), 'SUCCESS'
        )
