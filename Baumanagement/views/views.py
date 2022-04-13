import inspect
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig
from django_tables2.export import TableExport

from Baumanagement.models.abstract import add_search_field
from Baumanagement.models.models_comments import Comment
from Baumanagement.models.models_files import File
from Baumanagement.models.models_map import get_base_models
from Baumanagement.models.models_messages import MyMessage
from Baumanagement.models.models_projects import Project
from Baumanagement.models.models_settings import Settings


class CommentFormClass(ModelForm):
    class Meta:
        model = Comment
        fields = Comment.form_fields


def structure(request):
    return render(request, 'structure.html')


@login_required
def myrender(request, context):
    export_format = request.GET.get("_export", None)
    if export_format and TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, context['table1'])
        return exporter.response("table.{}".format(export_format))

    context['projects'] = Project.objects.all()
    context['settings'] = Settings.objects.get_or_create(user=request.user)[0]

    template = 'tables.html' if not request.GET else 'maintable.html'
    return render(request, template, context)


def my404(request, exception):
    return render(request, '404.html')


def upload_files(request, new_object):
    for file in request.FILES.getlist('file'):
        file_instance = File.objects.create(name=file.name, file=file, created_by=request.user)
        new_object.file_ids.append(file_instance.id)
        new_object.save(user=request.user)
        MyMessage.message(request, f'{file.name} {_("uploaded")}', 'SUCCESS')


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
    if not request.GET:
        context.setdefault('breadcrumbs_titel', baseClass._meta.verbose_name_plural)
        context.setdefault('breadcrumbs', [{'text': _("All")}])
        new_object_form(request, context, formClass)
        context['search_field'] = True
    else:
        if queryset is None:
            queryset = baseClass.objects
        dateFrom = request.GET.get('dateFrom')
        if dateFrom:
            queryset = queryset.filter(created__gte=datetime.strptime(dateFrom, "%Y-%m-%d"))
        dateTo = request.GET.get('dateTo')
        if dateTo:
            queryset = queryset.filter(created__lt=datetime.strptime(dateTo, "%Y-%m-%d") + timedelta(days=1))
        tag = request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tag=int(tag))

        project_id_str = request.GET.get('project')
        project_id = int(project_id_str) if project_id_str else None
        settings = Settings.objects.get_or_create(user=request.user)[0]
        settings_ap_id = settings.active_project.id if settings.active_project else None
        if project_id != settings_ap_id:
            settings.active_project = Project.objects.get(id=project_id) if project_id else None
            settings.save()
        if project_id and baseClass.__name__ == 'Contract':
            queryset = queryset.filter(project_id=project_id)
        elif project_id and baseClass.__name__ in ['Bill', 'Payment']:
            queryset = queryset.filter(contract__project_id=project_id)

        queryset = baseClass.extra_fields(queryset)
        queryset = add_search_field(queryset, request)
        table1 = tableClass(queryset, order_by="-created")
        RequestConfig(request).configure(table1)
        context['table1'] = table1


def generate_object_table(request, context, baseClass, tableClass, formClass, queryset):
    if not request.GET:
        context.setdefault('breadcrumbs_titel', baseClass._meta.verbose_name)
        edit_object_form(request, context, formClass, queryset.first())

        comment_ids = queryset.first().comment_ids
        comments = [{'object': Comment.objects.get(id=id), 'files': None} for id in comment_ids]
        for comment in comments:
            comment['files'] = [File.objects.get(id=id) for id in comment['object'].file_ids]
        context['tables'].append({'titel': _('Comments'), 'count': len(comment_ids),
                                  'comments': comments, 'form': CommentFormClass(), 'files_form': []})
    else:
        queryset = baseClass.extra_fields(queryset)
        table1 = tableClass(queryset, orderable=False, object_table=True)
        RequestConfig(request).configure(table1)
        context['table1'] = table1


def generate_next_objects_table(request, context, baseClass, tableClass, queryset, titel=None):
    queryset = baseClass.extra_fields(queryset)
    table = tableClass(queryset, order_by="-created", orderable=False)
    RequestConfig(request).configure(table)
    context['tables'].append({'table': table, 'titel': titel or baseClass._meta.verbose_name_plural,
                              'count': len(table.rows), 'link': f'{request.path}/{baseClass.urls}'})


def create_new_object_or_get_error(request, cls):
    if request.method != 'POST':
        return None
    formset = cls(request.POST, request.FILES)
    if formset.is_valid():
        new_object = formset.save(commit=False)
        new_object.created_by = request.user
        new_object.save()
        formset.save_m2m()
        MyMessage.message(request, f'{new_object.name} {_("created")}', 'SUCCESS')
        upload_files(request, new_object)
        add_comment_to_object(request, new_object)
        return None
    else:
        MyMessage.message(request, formset.errors, 'WARNING')
        return formset


def new_object_form(request, context, cls):
    error_form = create_new_object_or_get_error(request, cls)
    context['form'] = error_form or context.get('form') or cls()
    if 'FileModel' in str(inspect.getmro(cls.Meta.model)):
        context['files_form'] = []
    context['buttons'] = ['New']


def edit_object_form(request, context, cls, object):
    error_form = None
    if request.method == 'POST':
        if request.POST.get('createCopy'):
            error_form = create_new_object_or_get_error(request, cls)
        else:
            formset = cls(request.POST, request.FILES, instance=object)
            if formset.is_valid():
                object = formset.save(commit=False)
                object.save()
                formset.save_m2m()
                MyMessage.message(request, f'{object.name} {_("changed")}', 'SUCCESS')
                upload_files(request, object)
            else:
                MyMessage.message(request, formset.errors, 'WARNING')
            error_form = formset
    context['form'] = error_form or context.get('form') or cls(instance=object)
    if 'FileModel' in str(inspect.getmro(object.__class__)):
        context['files_form'] = object.files
    context['buttons'] = ['Edit']
