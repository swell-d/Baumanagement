import inspect

from django.db import IntegrityError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from comments.models import Comment
from files.models import File
from main.comments import CommentFormClass, add_comment_to_object
from main.models import add_search_field, get_or_none
from main.table_filters import filter_objects_table
from main.upload_files import upload_files
from notifications.models import Notification
from settings.models import Settings
from statistic.models import Visits, SearchQueries


def generate_objects_table(request, context, baseClass, tableClass, formClass, queryset=None):
    settings = context['settings']
    if 'created' in baseClass.table_fields:
        context['date_fields'] = True

    if not request.GET:
        context.setdefault('breadcrumbs_titel', baseClass._meta.verbose_name_plural)
        context.setdefault('breadcrumbs', [{'text': _("All")}])
        new_object_form(request, context, formClass)
        context['search_field'] = True
    # else:
    if queryset is None:
        queryset = baseClass.objects

    queryset = filter_objects_table(request, baseClass, queryset, settings)

    if request.GET.get('sort'):
        settings.sort[baseClass.urls] = request.GET.get('sort')
        settings.save()

    queryset = baseClass.extra_fields(queryset)
    queryset = add_search_field(queryset, request)
    table1 = tableClass(queryset, order_by=settings.sort.get(baseClass.urls, '-created'), settings=settings)
    RequestConfig(request).configure(table1)
    context['table1'] = table1


def generate_object_table(request, context, baseClass, tableClass, formClass, queryset):
    settings = context['settings']
    if not request.GET:
        context.setdefault('breadcrumbs_titel', baseClass._meta.verbose_name)
        edit_object_form(request, context, formClass, queryset.first())

        comments = []
        for comment in [get_or_none(Comment, id=id) for id in queryset.first().comment_ids]:
            if comment:
                comments.append({
                    'object': comment,
                    'files': list(filter(None, [get_or_none(File, id=id) for id in comment.file_ids]))
                })
        context['tables'].append({'titel': _('Comments'), 'count': len(comments),
                                  'comments': comments, 'form': CommentFormClass(), 'files_form': []})
    # else:
    queryset = baseClass.extra_fields(queryset)
    table1 = tableClass(queryset, orderable=False, object_table=True, settings=settings)
    RequestConfig(request).configure(table1)
    context['table1'] = table1


def generate_next_objects_table(request, context, baseClass, tableClass, queryset, titel=None):
    settings = context['settings']
    queryset = baseClass.extra_fields(queryset)
    table = tableClass(queryset, order_by=settings.sort.get(baseClass.urls, '-created'), settings=settings,
                       orderable=2)  # hack. ordered, but without a links in header
    RequestConfig(request).configure(table)
    context['tables'].append({'table': table, 'titel': titel or baseClass._meta.verbose_name_plural,
                              'count': len(table.rows), 'link': f'{request.path}/{baseClass.urls}'})


def create_new_object_or_get_error(request, cls):
    if request.method != 'POST':
        return None
    formset = cls(request.POST, request.FILES)
    if formset.is_valid():
        try:
            new_object = formset.save(commit=False)
            new_object.save()
            formset.save_m2m()
            verbose_name = new_object.verbose_name()
            link = reverse(new_object.url_id, args=[new_object.id])
            Notification.message(
                request, f'{verbose_name} "<a href="{link}">{new_object.name}</a>" ' + _("created"), 'SUCCESS'
            )
            upload_files(request, new_object)
            add_comment_to_object(request, new_object)
            return None
        except IntegrityError:
            Notification.message(request, _("Object already exist"), 'ERROR')
    else:
        Notification.message(request, formset.errors, 'ERROR')
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
        if request.POST.get('mainObject'):
            formset = cls(request.POST, request.FILES, instance=object)
            if formset.is_valid():
                object = formset.save(commit=False)
                object.save()
                formset.save_m2m()
                verbose_name = object.verbose_name()
                link = reverse(object.url_id, args=[object.id])
                Notification.message(
                    request, f'{verbose_name} "<a href="{link}">{object.name}</a>" ' + _("changed"), 'SUCCESS'
                )
                upload_files(request, object)
            else:
                Notification.message(request, formset.errors, 'ERROR')
            error_form = formset
        elif request.POST.get('createCopy'):
            error_form = create_new_object_or_get_error(request, cls)
        elif request.POST.get('editProducts'):
            pass
    context['form'] = error_form or context.get('form') or cls(instance=object)
    if 'FileModel' in str(inspect.getmro(object.__class__)):
        context['files_form'] = object.files
    context['buttons'] = ['Edit']


def get_base_context(request):
    visits = Visits.objects.get_or_create(page=request.path)[0]
    visits.count += 1
    visits.save()

    if request.GET.get("search"):
        searchquery = SearchQueries.objects.get_or_create(page=request.path, query=request.GET.get("search"))[0]
        searchquery.count += 1
        searchquery.save()

    return {'settings': Settings.objects.get_or_create(user=request.user)[0],
            'tables': []}


def labels(cls):
    return {'objects': [each for each in cls.objects.order_by('path') if each.count],
            'urls': cls.urls}
