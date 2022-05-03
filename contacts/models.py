from author.decorators import with_author
from django.db import models
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Company
from main.models import BaseModel, FileModel


@with_author
class Contact(BaseModel, FileModel):
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name=_('Company'),
                                on_delete=models.RESTRICT, related_name='contacts')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    email = models.EmailField(null=False, blank=True, verbose_name=_('E-mail'))
    phone = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Phone'))
    position = models.CharField(max_length=256, null=False, blank=True, verbose_name=_('Position'))

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    urls = 'contacts'
    url_id = 'contact_id'
    table_fields = 'company', 'name', 'email', 'phone', 'position', 'files'
    search_fields = 'company__name', 'name', 'email', 'phone', 'position'
    form_fields = 'open', 'company', 'name', 'email', 'phone', 'position'
