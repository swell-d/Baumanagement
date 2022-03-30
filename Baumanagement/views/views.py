from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_files import File


@login_required
def myrender(request, context):
    template = 'tables.html' if request.GET.get('search') is None else 'maintable.html'
    return render(request, template, context)


def upload_files(request, object):
    for file in request.FILES.getlist('file'):
        file_instance = File.objects.create(name=file.name, file=file)
        object.file_ids.append(file_instance.id)
        object.save()
        messages.success(request, f'{file.name} {_("uploaded")}')


def new_object_form(request, context, cls):
    if request.method == 'POST':
        formset = cls(request.POST, request.FILES)
        if formset.is_valid():
            new_object = cls.Meta.model(**formset.cleaned_data)
            new_object.save()
            messages.success(request, f'{new_object.name} {_("created")}')
            upload_files(request, new_object)
    context['form'] = cls()
    context['files_form'] = []
    context['buttons'] = ['New']


def edit_object_form(request, context, cls, object):
    if request.method == 'POST':
        formset = cls(request.POST, request.FILES, instance=object)
        if formset.is_valid():
            object.save()
            messages.success(request, f'{object.name} {_("changed")}')
            upload_files(request, object)
    context['form'] = cls(instance=object)
    context['files_form'] = object.files
    context['buttons'] = ['Edit']
