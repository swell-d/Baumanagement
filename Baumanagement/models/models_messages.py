from author.decorators import with_author
from django.contrib import messages
from django.contrib.messages import DEFAULT_TAGS, DEFAULT_LEVELS
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


@with_author
class MyMessage(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    name = models.TextField(null=False, blank=False, verbose_name=_('Message'))
    level = models.IntegerField(null=False, blank=False, verbose_name=_('Level'))
    open = models.BooleanField(default=True, null=False, blank=False, verbose_name=_('Open'))

    BOOTSTRAP_CLASSES = {
        10: 'text-warning',
        20: 'text-info',
        25: 'text-success',
        30: 'text-warning',
        40: 'alert-danger fw-bold',
    }

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return f'{self.created.strftime("%Y-%m-%d %H:%M")}  [{self.author}]  ' \
               f'{self.name}  ({self.level_tag()})'

    def level_tag(self):
        return DEFAULT_TAGS.get(self.level, "ERROR").upper()

    def bootstrap_class(self):
        return self.BOOTSTRAP_CLASSES.get(self.level, '')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @classmethod
    def message(cls, request, error, level='ERROR'):
        MyMessage.objects.create(author=request.user, name=error, level=DEFAULT_LEVELS.get(level, 40))

        error = format_html(error)
        if level == 'DEBUG':
            messages.debug(request, error)
        elif level == 'INFO':
            messages.info(request, error)
        elif level == 'SUCCESS':
            messages.success(request, error)
        elif level == 'WARNING':
            messages.warning(request, error)
        else:
            messages.error(request, error)

    urls = 'messages'
    table_fields = 'created', 'name', 'level'
    search_fields = 'name', 'level'
    form_fields = 'name', 'level'
