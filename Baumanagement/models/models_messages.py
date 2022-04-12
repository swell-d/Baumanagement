from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages import DEFAULT_TAGS, DEFAULT_LEVELS
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyMessage(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    name = models.TextField(null=False, blank=False, verbose_name=_('Message'))
    level = models.IntegerField(null=False, blank=False, verbose_name=_('Level'))

    def __str__(self):
        return f'{self.created.strftime("%Y-%m-%d %H:%M")}  [{self.created_by}]  ' \
               f'{self.name}  ({DEFAULT_TAGS.get(self.level, "error").upper()})'

    @classmethod
    def message(cls, request, error, level='ERROR'):
        MyMessage.objects.create(created_by=request.user, name=error, level=DEFAULT_LEVELS.get(level, 40))
        if level == 'DEBUG':
            messages.debug(request, error)
        elif level == 'INFO':
            messages.info(request, error)
        elif level == 'SUCCESS':
            messages.success(request, error)
        elif level == 'WARNING':
            messages.warning(request, error)
        elif level == 'ERROR':
            messages.error(request, error)
