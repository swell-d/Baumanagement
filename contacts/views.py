from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Company
from contacts.models import Contact
from contacts.tables import ContactTable
from main.views import get_base_context, generate_objects_table, myrender, generate_object_table, \
    generate_next_objects_table

baseClass = Contact
tableClass = ContactTable


class FormClass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(open=True)

    class Meta:
        model = baseClass
        fields = baseClass.form_fields


@login_required
def objects_table(request):
    context = get_base_context(request)
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


@login_required
def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    if queryset.first() is None:
        raise Http404
    contact = queryset.first()

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_contacts', args=[contact.company.id]),
                               'text': contact.company.name},
                              {'text': contact.name}]

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


@login_required
def company_contacts(request, id):
    context = get_base_context(request)
    company = get_object_or_404(Company, id=id)
    queryset = company.contacts.all()

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': company.name}]

    form = FormClass()
    form.fields["company"].initial = company
    form.fields['company'].queryset = Company.objects.filter(id=id)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_contacts_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
