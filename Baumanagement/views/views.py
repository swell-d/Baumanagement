import inspect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import NotSupportedError
from django.db.models import QuerySet
from django.forms import ModelForm
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.abstract import add_search_field
from Baumanagement.models.models_comments import Comment
from Baumanagement.models.models_files import File
from Baumanagement.models.models_map import get_base_models


class CommentFormClass(ModelForm):
    class Meta:
        model = Comment
        fields = Comment.form_fields


@login_required
def myrender(request, context):
    template = 'tables.html' if request.GET.get('search') is None else 'maintable.html'
    return render(request, template, context)


def upload_files(request, new_object):
    for file in request.FILES.getlist('file'):
        file_instance = File.objects.create(name=file.name, file=file)
        new_object.file_ids.append(file_instance.id)
        new_object.save()
        messages.success(request, f'{file.name} {_("uploaded")}')


def add_comment_to_object(request, new_object):
    path = request.POST.get('newCommentNextURL')
    if path:
        object_name, id = path[4:].split('/')
        if '?' in id:
            id = id[:id.find('?')]
        base_models = get_base_models()
        obj = base_models[object_name].objects.get(id=int(id))
        obj.comment_ids.append(new_object.id)
        obj.save()


def generate_objects_table(request, context, baseClass, tableClass, formClass, queryset=None):
    context.setdefault('titel1', f'{_("All")} {baseClass._meta.verbose_name_plural}')
    queryset = queryset or baseClass.objects
    new_object_form(request, context, formClass)
    queryset = baseClass.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = tableClass(queryset, order_by="-created", orderable=request.GET.get('search') is None)
    RequestConfig(request).configure(table1)
    context['table1'] = table1


def generate_object_table(request, context, baseClass, tableClass, formClass, queryset):
    context.setdefault('titel1', f'{baseClass._meta.verbose_name} - {queryset.first().name}')
    edit_object_form(request, context, formClass, queryset.first())
    queryset = baseClass.extra_fields(queryset)
    table1 = tableClass(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1
    comment_ids = queryset.first().comment_ids
    comments = [{'object': Comment.objects.get(id=id), 'files': None} for id in comment_ids]
    for comment in comments:
        comment['files'] = [File.objects.get(id=id) for id in comment['object'].file_ids]
    context['tables'].append({'titel': _('Comments'), 'count': len(comment_ids),
                              'comments': comments, 'form': CommentFormClass(), 'files_form': []})


def generate_next_objects_table(request, context, baseClass, tableClass, queryset):
    try:
        queryset = baseClass.extra_fields(queryset)
    except (NotSupportedError, AttributeError):
        pass
    table = tableClass(queryset, order_by="-created", orderable=False)
    RequestConfig(request).configure(table)
    context['tables'].append({'table': table, 'titel': baseClass._meta.verbose_name_plural, 'count': len(table.rows)})


def new_object_form(request, context, cls):
    if request.method == 'POST':
        formset = cls(request.POST, request.FILES)
        if formset.is_valid():
            many_to_many_fields = {}
            for key, value in formset.cleaned_data.copy().items():
                if isinstance(value, QuerySet):
                    many_to_many_fields[key] = value
                    formset.cleaned_data.pop(key)
            new_object = cls.Meta.model(**formset.cleaned_data)
            new_object.save()
            if many_to_many_fields:
                new_object.role.set(many_to_many_fields['role'])
                new_object.save()
            messages.success(request, f'{new_object.name} {_("created")}')
            upload_files(request, new_object)
        add_comment_to_object(request, new_object)
    context['form'] = cls()
    if 'FileModel' in str(inspect.getmro(cls.Meta.model)):
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
    if 'FileModel' in str(inspect.getmro(object.__class__)):
        context['files_form'] = object.files
    context['buttons'] = ['Edit']
